import os
import time
import requests
import hashlib
import http.client
import traceback
import threading
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed

CHUNK_DOWNLOAD_RETRY_DELAY = 2
MAX_CHUNK_DOWNLOAD_RETRIES = 1
DOWNLOAD_CHUNK_SIZE_ITER = 1024 * 256  


def _download_individual_chunk(chunk_url, temp_file_path, start_byte, end_byte, headers,
                               part_num, total_parts, progress_data, cancellation_event, skip_event, pause_event, global_emit_time_ref, cookies_for_chunk,
                               logger_func, emitter=None, api_original_filename=None):
    if cancellation_event and cancellation_event.is_set():
        logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Download cancelled before start.")
        return 0, False
    if skip_event and skip_event.is_set():
        logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Skip event triggered before start.")
        return 0, False

    if pause_event and pause_event.is_set():
        logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Download paused before start...")
        while pause_event.is_set():
            if cancellation_event and cancellation_event.is_set():
                logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Download cancelled while paused.")
                return 0, False
            time.sleep(0.2)
        logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Download resumed.")

    chunk_headers = headers.copy()
    if end_byte != -1 :
        chunk_headers['Range'] = f"bytes={start_byte}-{end_byte}"
    elif start_byte == 0 and end_byte == -1:
        pass

    bytes_this_chunk = 0
    last_speed_calc_time = time.time()
    bytes_at_last_speed_calc = 0

    for attempt in range(MAX_CHUNK_DOWNLOAD_RETRIES + 1):
        if cancellation_event and cancellation_event.is_set():
            logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Cancelled during retry loop.")
            return bytes_this_chunk, False
        if skip_event and skip_event.is_set():
            logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Skip event during retry loop.")
            return bytes_this_chunk, False
        if pause_event and pause_event.is_set():
            logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Paused during retry loop...")
            while pause_event.is_set():
                if cancellation_event and cancellation_event.is_set():
                    logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Cancelled while paused in retry loop.")
                    return bytes_this_chunk, False
                time.sleep(0.2)
            logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Resumed from retry loop pause.")

        try:
            if attempt > 0:
                logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Retrying download (Attempt {attempt}/{MAX_CHUNK_DOWNLOAD_RETRIES})...")
                time.sleep(CHUNK_DOWNLOAD_RETRY_DELAY * (2 ** (attempt - 1)))
                last_speed_calc_time = time.time()
                bytes_at_last_speed_calc = bytes_this_chunk
            log_msg = f"   🚀 [Chunk {part_num + 1}/{total_parts}] Starting download: bytes {start_byte}-{end_byte if end_byte != -1 else 'EOF'}"
            logger_func(log_msg)
            response = requests.get(chunk_url, headers=chunk_headers, timeout=(10, 120), stream=True, cookies=cookies_for_chunk)
            response.raise_for_status()
            if start_byte == 0 and end_byte == -1 and int(response.headers.get('Content-Length', 0)) == 0:
                logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Confirmed 0-byte file.")
                with progress_data['lock']:
                    progress_data['chunks_status'][part_num]['active'] = False
                    progress_data['chunks_status'][part_num]['speed_bps'] = 0
                return 0, True

            with open(temp_file_path, 'r+b') as f:
                f.seek(start_byte)
                for data_segment in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE_ITER):
                    if cancellation_event and cancellation_event.is_set():
                        logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Cancelled during data iteration.")
                        return bytes_this_chunk, False
                    if skip_event and skip_event.is_set():
                        logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Skip event during data iteration.")
                        return bytes_this_chunk, False
                    if pause_event and pause_event.is_set():
                        logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Paused during data iteration...")
                        while pause_event.is_set():
                            if cancellation_event and cancellation_event.is_set():
                                logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Cancelled while paused in data iteration.")
                                return bytes_this_chunk, False
                            time.sleep(0.2)
                        logger_func(f"   [Chunk {part_num + 1}/{total_parts}] Resumed from data iteration pause.")
                    if data_segment:
                        f.write(data_segment)
                        bytes_this_chunk += len(data_segment)
                        
                        with progress_data['lock']:
                            progress_data['total_downloaded_so_far'] += len(data_segment)
                            progress_data['chunks_status'][part_num]['downloaded'] = bytes_this_chunk
                            progress_data['chunks_status'][part_num]['active'] = True

                            current_time = time.time()
                            time_delta_speed = current_time - last_speed_calc_time
                            if time_delta_speed > 0.5:
                                bytes_delta = bytes_this_chunk - bytes_at_last_speed_calc
                                current_speed_bps = (bytes_delta * 8) / time_delta_speed if time_delta_speed > 0 else 0
                                progress_data['chunks_status'][part_num]['speed_bps'] = current_speed_bps
                                last_speed_calc_time = current_time
                                bytes_at_last_speed_calc = bytes_this_chunk                            
                            if emitter and (current_time - global_emit_time_ref[0] > 0.25):
                                global_emit_time_ref[0] = current_time
                                status_list_copy = [dict(s) for s in progress_data['chunks_status']]
                                if isinstance(emitter, queue.Queue):
                                    emitter.put({'type': 'file_progress', 'payload': (api_original_filename, status_list_copy)})
                                elif hasattr(emitter, 'file_progress_signal'):
                                    emitter.file_progress_signal.emit(api_original_filename, status_list_copy)
            return bytes_this_chunk, True

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, http.client.IncompleteRead) as e:
            logger_func(f"   ❌ [Chunk {part_num + 1}/{total_parts}] Retryable error: {e}")
            if isinstance(e, requests.exceptions.ConnectionError) and \
               ("Failed to resolve" in str(e) or "NameResolutionError" in str(e)):
                logger_func("   💡 This looks like a DNS resolution problem. Please check your internet connection, DNS settings, or VPN.")
            if attempt == MAX_CHUNK_DOWNLOAD_RETRIES:
                logger_func(f"   ❌ [Chunk {part_num + 1}/{total_parts}] Failed after {MAX_CHUNK_DOWNLOAD_RETRIES} retries.")
                return bytes_this_chunk, False
        except requests.exceptions.RequestException as e:
            logger_func(f"   ❌ [Chunk {part_num + 1}/{total_parts}] Non-retryable error: {e}")
            if ("Failed to resolve" in str(e) or "NameResolutionError" in str(e)):
                logger_func("   💡 This looks like a DNS resolution problem. Please check your internet connection, DNS settings, or VPN.")
            return bytes_this_chunk, False
        except Exception as e:
            logger_func(f"   ❌ [Chunk {part_num + 1}/{total_parts}] Unexpected error: {e}\n{traceback.format_exc(limit=1)}")

            return bytes_this_chunk, False
    with progress_data['lock']:
        progress_data['chunks_status'][part_num]['active'] = False
        progress_data['chunks_status'][part_num]['speed_bps'] = 0
    return bytes_this_chunk, False


def download_file_in_parts(file_url, save_path, total_size, num_parts, headers, api_original_filename,
                           emitter_for_multipart, cookies_for_chunk_session,
                           cancellation_event, skip_event, logger_func, pause_event):
    logger_func(f"⬇️ Initializing Multi-part Download ({num_parts} parts) for: '{api_original_filename}' (Size: {total_size / (1024*1024):.2f} MB)")
    temp_file_path = save_path + ".part"

    try:
        with open(temp_file_path, 'wb') as f_temp:
            if total_size > 0:
                f_temp.truncate(total_size)
    except IOError as e:
        logger_func(f"   ❌ Error creating/truncating temp file '{temp_file_path}': {e}")
        return False, 0, None, None

    chunk_size_calc = total_size // num_parts
    chunks_ranges = []
    for i in range(num_parts):
        start = i * chunk_size_calc
        end = start + chunk_size_calc - 1 if i < num_parts - 1 else total_size - 1
        if start <= end:
            chunks_ranges.append((start, end))
        elif total_size == 0 and i == 0:
            chunks_ranges.append((0, -1))

    chunk_actual_sizes = []
    for start, end in chunks_ranges:
        if end == -1 and start == 0:
            chunk_actual_sizes.append(0)
        else:
            chunk_actual_sizes.append(end - start + 1)

    if not chunks_ranges and total_size > 0:
        logger_func(f"   ⚠️ No valid chunk ranges for multipart download of '{api_original_filename}'. Aborting multipart.")
        if os.path.exists(temp_file_path): os.remove(temp_file_path)
        return False, 0, None, None

    progress_data = {
        'total_file_size': total_size,
        'total_downloaded_so_far': 0,
        'chunks_status': [
            {'id': i, 'downloaded': 0, 'total': chunk_actual_sizes[i] if i < len(chunk_actual_sizes) else 0, 'active': False, 'speed_bps': 0.0}
            for i in range(num_parts)
        ],
        'lock': threading.Lock(),
        'last_global_emit_time': [time.time()]
    }

    chunk_futures = []
    all_chunks_successful = True
    total_bytes_from_chunks = 0

    with ThreadPoolExecutor(max_workers=num_parts, thread_name_prefix=f"MPChunk_{api_original_filename[:10]}_") as chunk_pool:
        for i, (start, end) in enumerate(chunks_ranges):
            if cancellation_event and cancellation_event.is_set(): all_chunks_successful = False; break
            chunk_futures.append(chunk_pool.submit(
                _download_individual_chunk, chunk_url=file_url, temp_file_path=temp_file_path,
                start_byte=start, end_byte=end, headers=headers, part_num=i, total_parts=num_parts,
                progress_data=progress_data, cancellation_event=cancellation_event, skip_event=skip_event, global_emit_time_ref=progress_data['last_global_emit_time'],
                pause_event=pause_event, cookies_for_chunk=cookies_for_chunk_session, logger_func=logger_func, emitter=emitter_for_multipart,
                api_original_filename=api_original_filename
            ))

        for future in as_completed(chunk_futures):
            if cancellation_event and cancellation_event.is_set(): all_chunks_successful = False; break
            bytes_downloaded_this_chunk, success_this_chunk = future.result()
            total_bytes_from_chunks += bytes_downloaded_this_chunk
            if not success_this_chunk:
                all_chunks_successful = False

    if cancellation_event and cancellation_event.is_set():
        logger_func(f"   Multi-part download for '{api_original_filename}' cancelled by main event.")
        all_chunks_successful = False
    if emitter_for_multipart:
        with progress_data['lock']:
            status_list_copy = [dict(s) for s in progress_data['chunks_status']]
            if isinstance(emitter_for_multipart, queue.Queue):
                emitter_for_multipart.put({'type': 'file_progress', 'payload': (api_original_filename, status_list_copy)})
            elif hasattr(emitter_for_multipart, 'file_progress_signal'):
                emitter_for_multipart.file_progress_signal.emit(api_original_filename, status_list_copy)

    if all_chunks_successful and (total_bytes_from_chunks == total_size or total_size == 0):
        logger_func(f"   ✅ Multi-part download successful for '{api_original_filename}'. Total bytes: {total_bytes_from_chunks}")
        md5_hasher = hashlib.md5()
        with open(temp_file_path, 'rb') as f_hash:
            for buf in iter(lambda: f_hash.read(4096*10), b''):
                md5_hasher.update(buf)
        calculated_hash = md5_hasher.hexdigest()
        return True, total_bytes_from_chunks, calculated_hash, open(temp_file_path, 'rb')
    else:
        logger_func(f"   ❌ Multi-part download failed for '{api_original_filename}'. Success: {all_chunks_successful}, Bytes: {total_bytes_from_chunks}/{total_size}. Cleaning up.")
        if os.path.exists(temp_file_path):
            try: os.remove(temp_file_path)
            except OSError as e: logger_func(f"    Failed to remove temp part file '{temp_file_path}': {e}")
        return False, total_bytes_from_chunks, None, None