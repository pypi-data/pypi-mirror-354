
translations ={
"en":{
"settings_dialog_title":"Settings",
"language_label":"Language:",
"lang_english":"English",
"lang_japanese":"日本語 (Japanese)",
"theme_toggle_light":"Switch to Light Mode",
"theme_toggle_dark":"Switch to Dark Mode",
"theme_tooltip_light":"Change the application appearance to light.",
"theme_tooltip_dark":"Change the application appearance to dark.",
"ok_button":"OK",
"appearance_group_title":"Appearance",
"language_group_title":"Language Settings",
"creator_post_url_label":"🔗 Kemono Creator/Post URL:",
"download_location_label":"📁 Download Location:",
"filter_by_character_label":"🎯 Filter by Character(s) (comma-separated):",
"skip_with_words_label":"🚫 Skip with Words (comma-separated):",
"remove_words_from_name_label":"✂️ Remove Words from name:",
"filter_all_radio":"All",
"filter_images_radio":"Images/GIFs",
"filter_videos_radio":"Videos",
"filter_archives_radio":"📦 Only Archives",
"filter_links_radio":"🔗 Only Links",
"filter_audio_radio":"🎧 Only Audio",
"favorite_mode_checkbox_label":"⭐ Favorite Mode",
"browse_button_text":"Browse...",
"char_filter_scope_files_text":"Filter: Files",
"char_filter_scope_files_tooltip":"Current Scope: Files\n\nFilters individual files by name. A post is kept if any file matches.\nOnly matching files from that post are downloaded.\nExample: Filter 'Tifa'. File 'Tifa_artwork.jpg' matches and is downloaded.\nFolder Naming: Uses character from matching filename.\n\nClick to cycle to: Both",
"char_filter_scope_title_text":"Filter: Title",
"char_filter_scope_title_tooltip":"Current Scope: Title\n\nFilters entire posts by their title. All files from a matching post are downloaded.\nExample: Filter 'Aerith'. Post titled 'Aerith's Garden' matches; all its files are downloaded.\nFolder Naming: Uses character from matching post title.\n\nClick to cycle to: Files",
"char_filter_scope_both_text":"Filter: Both",
"char_filter_scope_both_tooltip":"Current Scope: Both (Title then Files)\n\n1. Checks post title: If matches, all files from post are downloaded.\n2. If title doesn't match, checks filenames: If any file matches, only that file is downloaded.\nExample: Filter 'Cloud'.\n - Post 'Cloud Strife' (title match) -> all files downloaded.\n - Post 'Bike Chase' with 'Cloud_fenrir.jpg' (file match) -> only 'Cloud_fenrir.jpg' downloaded.\nFolder Naming: Prioritizes title match, then file match.\n\nClick to cycle to: Comments",
"char_filter_scope_comments_text":"Filter: Comments (Beta)",
"char_filter_scope_comments_tooltip":"Current Scope: Comments (Beta - Files first, then Comments as fallback)\n\n1. Checks filenames: If any file in the post matches the filter, the entire post is downloaded. Comments are NOT checked for this filter term.\n2. If no file matches, THEN checks post comments: If a comment matches, the entire post is downloaded.\nExample: Filter 'Barret'.\n - Post A: Files 'Barret_gunarm.jpg', 'other.png'. File 'Barret_gunarm.jpg' matches. All files from Post A downloaded. Comments not checked for 'Barret'.\n - Post B: Files 'dyne.jpg', 'weapon.gif'. Comments: '...a drawing of Barret Wallace...'. No file match for 'Barret'. Comment matches. All files from Post B downloaded.\nFolder Naming: Prioritizes character from file match, then from comment match.\n\nClick to cycle to: Title",
"char_filter_scope_unknown_text":"Filter: Unknown",
"char_filter_scope_unknown_tooltip":"Current Scope: Unknown\n\nThe character filter scope is in an unknown state. Please cycle or reset.\n\nClick to cycle to: Title",
"skip_words_input_tooltip":"Enter words, comma-separated, to skip downloading certain content (e.g., WIP, sketch, preview).\n\n"  "The 'Scope: [Type]' button next to this input cycles how this filter applies:\n"  "- Scope: Files: Skips individual files if their names contain any of these words.\n"  "- Scope: Posts: Skips entire posts if their titles contain any of these words.\n"  "- Scope: Both: Applies both (post title first, then individual files if post title is okay).",
"remove_words_input_tooltip":
"Enter words, comma-separated, to remove from downloaded filenames (case-insensitive).\n"
"Useful for cleaning up common prefixes/suffixes.\n"
"Example: patreon, kemono, [HD], _final",
"skip_scope_files_text":"Scope: Files",
"skip_scope_files_tooltip":"Current Skip Scope: Files\n\nSkips individual files if their names contain any of the 'Skip with Words'.\nExample: Skip words \"WIP, sketch\".\n- File \"art_WIP.jpg\" -> SKIPPED.\n- File \"final_art.png\" -> DOWNLOADED (if other conditions met).\n\nPost is still processed for other non-skipped files.\nClick to cycle to: Both",
"skip_scope_posts_text":"Scope: Posts",
"skip_scope_posts_tooltip":"Current Skip Scope: Posts\n\nSkips entire posts if their titles contain any of the 'Skip with Words'.\nAll files from a skipped post are ignored.\nExample: Skip words \"preview, announcement\".\n- Post \"Exciting Announcement!\" -> SKIPPED.\n- Post \"Finished Artwork\" -> PROCESSED (if other conditions met).\n\nClick to cycle to: Files",
"skip_scope_both_text":"Scope: Both",
"skip_scope_both_tooltip":"Current Skip Scope: Both (Posts then Files)\n\n1. Checks post title: If title contains a skip word, the entire post is SKIPPED.\n2. If post title is OK, then checks individual filenames: If a filename contains a skip word, only that file is SKIPPED.\nExample: Skip words \"WIP, sketch\".\n- Post \"Sketches and WIPs\" (title match) -> ENTIRE POST SKIPPED.\n- Post \"Art Update\" (title OK) with files:\n    - \"character_WIP.jpg\" (file match) -> SKIPPED.\n    - \"final_scene.png\" (file OK) -> DOWNLOADED.\n\nClick to cycle to: Posts",
"skip_scope_unknown_text":"Scope: Unknown",
"skip_scope_unknown_tooltip":"Current Skip Scope: Unknown\n\nThe skip words scope is in an unknown state. Please cycle or reset.\n\nClick to cycle to: Posts",
"language_change_title":"Language Changed",
"language_change_message":"The language has been changed. A restart is required for all changes to take full effect.",
"language_change_informative":"Would you like to restart the application now?",
"restart_now_button":"Restart Now",
"skip_zip_checkbox_label":"Skip .zip",
"skip_rar_checkbox_label":"Skip .rar",
"download_thumbnails_checkbox_label":"Download Thumbnails Only",
"scan_content_images_checkbox_label":"Scan Content for Images",
"compress_images_checkbox_label":"Compress to WebP",
"separate_folders_checkbox_label":"Separate Folders by Name/Title",
"subfolder_per_post_checkbox_label":"Subfolder per Post",
"use_cookie_checkbox_label":"Use Cookie",
"use_multithreading_checkbox_base_label":"Use Multithreading",
"show_external_links_checkbox_label":"Show External Links in Log",
"manga_comic_mode_checkbox_label":"Manga/Comic Mode",
"threads_label":"Threads:",
"start_download_button_text":"⬇️ Start Download",
"start_download_button_tooltip":"Click to start the download or link extraction process with the current settings.",
"extract_links_button_text":"🔗 Extract Links",
"pause_download_button_text":"⏸️ Pause Download",
"pause_download_button_tooltip":"Click to pause the ongoing download process.",
"resume_download_button_text":"▶️ Resume Download",
"resume_download_button_tooltip":"Click to resume the download.",
"cancel_button_text":"❌ Cancel & Reset UI",
"cancel_button_tooltip":"Click to cancel the ongoing download/extraction process and reset the UI fields (preserving URL and Directory).",
"error_button_text":"Error",
"error_button_tooltip":"View files skipped due to errors and optionally retry them.",
"cancel_retry_button_text":"❌ Cancel Retry",
"known_chars_label_text":"🎭 Known Shows/Characters (for Folder Names):",
"open_known_txt_button_text":"Open Known.txt",
"known_chars_list_tooltip":"This list contains names used for automatic folder creation when 'Separate Folders' is on\nand no specific 'Filter by Character(s)' is provided or matches a post.\nAdd names of series, games, or characters you frequently download.",
"open_known_txt_button_tooltip":"Open the 'Known.txt' file in your default text editor.\nThe file is located in the application's directory.",
"add_char_button_text":"➕ Add",
"add_char_button_tooltip":"Add the name from the input field to the 'Known Shows/Characters' list.",
"add_to_filter_button_text":"⤵️ Add to Filter",
"add_to_filter_button_tooltip":"Select names from 'Known Shows/Characters' list to add to the 'Filter by Character(s)' field above.",
"delete_char_button_text":"🗑️ Delete Selected",
"delete_char_button_tooltip":"Delete the selected name(s) from the 'Known Shows/Characters' list.",
"progress_log_label_text":"📜 Progress Log:",
"radio_all_tooltip":"Download all file types found in posts.",
"radio_images_tooltip":"Download only common image formats (JPG, PNG, GIF, WEBP, etc.).",
"radio_videos_tooltip":"Download only common video formats (MP4, MKV, WEBM, MOV, etc.).",
"radio_only_archives_tooltip":"Exclusively download .zip and .rar files. Other file-specific options are disabled.",
"radio_only_audio_tooltip":"Download only common audio formats (MP3, WAV, FLAC, etc.).",
"radio_only_links_tooltip":"Extract and display external links from post descriptions instead of downloading files.\nDownload-related options will be disabled.",
"favorite_mode_checkbox_tooltip":"Enable Favorite Mode to browse saved artists/posts.\nThis will replace the URL input with Favorite selection buttons.",
"skip_zip_checkbox_tooltip":"If checked, .zip archive files will not be downloaded.\n(Disabled if 'Only Archives' is selected).",
"skip_rar_checkbox_tooltip":"If checked, .rar archive files will not be downloaded.\n(Disabled if 'Only Archives' is selected).",
"download_thumbnails_checkbox_tooltip":"Downloads small preview images from the API instead of full-sized files (if available).\nIf 'Scan Post Content for Image URLs' is also checked, this mode will *only* download images found by the content scan (ignoring API thumbnails).",
"scan_content_images_checkbox_tooltip":"If checked, the downloader will scan the HTML content of posts for image URLs (from <img> tags or direct links).\nThis includes resolving relative paths from <img> tags to full URLs.\nRelative paths in <img> tags (e.g., /data/image.jpg) will be resolved to full URLs.\nUseful for cases where images are in the post description but not in the API's file/attachment list.",
"compress_images_checkbox_tooltip":"Compress images > 1.5MB to WebP format (requires Pillow).",
"use_subfolders_checkbox_tooltip":"Create subfolders based on 'Filter by Character(s)' input or post titles.\nUses 'Known Shows/Characters' list as a fallback for folder names if no specific filter matches.\nEnables the 'Filter by Character(s)' input and 'Custom Folder Name' for single posts.",
"use_subfolder_per_post_checkbox_tooltip":"Creates a subfolder for each post. If 'Separate Folders' is also on, it's inside the character/title folder.",
"use_cookie_checkbox_tooltip":"If checked, will attempt to use cookies from 'cookies.txt' (Netscape format)\nin the application directory for requests.\nUseful for accessing content that requires login on Kemono/Coomer.",
"cookie_text_input_tooltip":"Enter your cookie string directly.\nThis will be used if 'Use Cookie' is checked AND 'cookies.txt' is not found or this field is not empty.\nThe format depends on how the backend will parse it (e.g., 'name1=value1; name2=value2').",
"use_multithreading_checkbox_tooltip":"Enables concurrent operations. See 'Threads' input for details.",
"thread_count_input_tooltip":(
"Number of concurrent operations.\n- Single Post: Concurrent file downloads (1-10 recommended).\n"
"- Creator Feed URL: Number of posts to process simultaneously (1-200 recommended).\n"
"  Files within each post are downloaded one by one by its worker.\nIf 'Use Multithreading' is unchecked, 1 thread is used."),
"external_links_checkbox_tooltip":"If checked, a secondary log panel appears below the main log to display external links found in post descriptions.\n(Disabled if 'Only Links' or 'Only Archives' mode is active).",
"manga_mode_checkbox_tooltip":"Downloads posts from oldest to newest and renames files based on post title (for creator feeds only).","multipart_on_button_text":"Multi-part: ON",
"multipart_on_button_tooltip":"Multi-part Download: ON\n\nEnables downloading large files in multiple segments simultaneously.\n- Can speed up downloads for single large files (e.g., videos).\n- May increase CPU/network usage.\n- For feeds with many small files, this might not offer speed benefits and could make UI/log busy.\n- If multi-part fails, it retries as single-stream.\n\nClick to turn OFF.",
"multipart_off_button_text":"Multi-part: OFF",
"multipart_off_button_tooltip":"Multi-part Download: OFF\n\nAll files downloaded using a single stream.\n- Stable and works well for most scenarios, especially many smaller files.\n- Large files downloaded sequentially.\n\nClick to turn ON (see advisory).",
"reset_button_text":"🔄 Reset",
"reset_button_tooltip":"Reset all inputs and logs to default state (only when idle).",
"progress_idle_text":"Progress: Idle",
"missed_character_log_label_text":"🚫 Missed Character Log:",
"creator_popup_title":"Creator Selection",
"creator_popup_search_placeholder":"Search by name, service, or paste creator URL...",
"creator_popup_add_selected_button":"Add Selected",
"creator_popup_scope_characters_button":"Scope: Characters",
"creator_popup_scope_creators_button":"Scope: Creators",
"favorite_artists_button_text":"🖼️ Favorite Artists",
"favorite_artists_button_tooltip":"Browse and download from your favorite artists on Kemono.su/Coomer.su.",
"favorite_posts_button_text":"📄 Favorite Posts",
"favorite_posts_button_tooltip":"Browse and download your favorite posts from Kemono.su/Coomer.su.",
"favorite_scope_selected_location_text":"Scope: Selected Location",
"favorite_scope_selected_location_tooltip":"Current Favorite Download Scope: Selected Location\n\nAll selected favorite artists/posts will be downloaded into the main 'Download Location' specified in the UI.\nFilters (character, skip words, file type) will apply globally to all content.\n\nClick to change to: Artist Folders",
"favorite_scope_artist_folders_text":"Scope: Artist Folders",
"favorite_scope_artist_folders_tooltip":"Current Favorite Download Scope: Artist Folders\n\nFor each selected favorite artist/post, a new subfolder (named after the artist) will be created inside the main 'Download Location'.\nContent for that artist/post will be downloaded into their specific subfolder.\nFilters (character, skip words, file type) will apply *within* each artist's folder.\n\nClick to change to: Selected Location",
"favorite_scope_unknown_text":"Scope: Unknown",
"favorite_scope_unknown_tooltip":"Favorite download scope is unknown. Click to cycle.",
"manga_style_post_title_text":"Name: Post Title",
"manga_style_original_file_text":"Name: Original File",
"manga_style_date_based_text":"Name: Date Based",
"manga_style_title_global_num_text":"Name: Title+G.Num",
"manga_style_unknown_text":"Name: Unknown Style",
"fav_artists_dialog_title":"Favorite Artists",
"fav_artists_loading_status":"Loading favorite artists...",
"fav_artists_search_placeholder":"Search artists...",
"fav_artists_select_all_button":"Select All",
"fav_artists_deselect_all_button":"Deselect All",
"fav_artists_download_selected_button":"Download Selected",
"fav_artists_cancel_button":"Cancel",
"fav_artists_loading_from_source_status":"⏳ Loading favorites from {source_name}...",
"fav_artists_found_status":"Found {count} total favorite artist(s).",
"fav_artists_none_found_status":"No favorite artists found on Kemono.su or Coomer.su.",
"fav_artists_failed_status":"Failed to fetch favorites.",
"fav_artists_cookies_required_status":"Error: Cookies enabled but could not be loaded for any source.",
"fav_artists_no_favorites_after_processing":"No favorite artists found after processing.",
"fav_artists_no_selection_title":"No Selection",
"fav_artists_no_selection_message":"Please select at least one artist to download.",

"fav_posts_dialog_title":"Favorite Posts",
"fav_posts_loading_status":"Loading favorite posts...",
"fav_posts_search_placeholder":"Search posts (title, creator, ID, service)...",
"fav_posts_select_all_button":"Select All",
"fav_posts_deselect_all_button":"Deselect All",
"fav_posts_download_selected_button":"Download Selected",
"fav_posts_cancel_button":"Cancel",
"fav_posts_cookies_required_error":"Error: Cookies are required for favorite posts but could not be loaded.",
"fav_posts_auth_failed_title":"Authorization Failed (Posts)",
"fav_posts_auth_failed_message":"Could not fetch favorites{domain_specific_part} due to an authorization error:\n\n{error_message}\n\nThis usually means your cookies are missing, invalid, or expired for the site. Please check your cookie setup.",
"fav_posts_fetch_error_title":"Fetch Error",
"fav_posts_fetch_error_message":"Error fetching favorites from {domain}{error_message_part}",
"fav_posts_no_posts_found_status":"No favorite posts found.",
"fav_posts_found_status":"{count} favorite post(s) found.",
"fav_posts_display_error_status":"Error displaying posts: {error}",
"fav_posts_ui_error_title":"UI Error",
"fav_posts_ui_error_message":"Could not display favorite posts: {error}",
"fav_posts_auth_failed_message_generic":"Could not fetch favorites{domain_specific_part} due to an authorization error. This usually means your cookies are missing, invalid, or expired for the site. Please check your cookie setup.",
"key_fetching_fav_post_list_init":"Fetching list of favorite posts...",
"key_fetching_from_source_kemono_su":"Fetching favorites from Kemono.su...",
"key_fetching_from_source_coomer_su":"Fetching favorites from Coomer.su...",
"fav_posts_fetch_cancelled_status":"Favorite post fetch cancelled.",

"known_names_filter_dialog_title":"Add Known Names to Filter",
"known_names_filter_search_placeholder":"Search names...",
"known_names_filter_select_all_button":"Select All",
"known_names_filter_deselect_all_button":"Deselect All",
"known_names_filter_add_selected_button":"Add Selected",

"error_files_dialog_title":"Files Skipped Due to Errors",
"error_files_no_errors_label":"No files were recorded as skipped due to errors in the last session or after retries.",
"error_files_found_label":"The following {count} file(s) were skipped due to download errors:",
"error_files_select_all_button":"Select All",
"error_files_retry_selected_button":"Retry Selected",
"error_files_export_urls_button":"Export URLs to .txt",
"error_files_no_selection_retry_message":"Please select at least one file to retry.",
"error_files_no_errors_export_title":"No Errors",
"error_files_no_errors_export_message":"There are no error file URLs to export.",
"error_files_no_urls_found_export_title":"No URLs Found",
"error_files_no_urls_found_export_message":"Could not extract any URLs from the error file list to export.",
"error_files_save_dialog_title":"Save Error File URLs",
"error_files_export_success_title":"Export Successful",
"error_files_export_success_message":"Successfully exported {count} entries to:\n{filepath}",
"error_files_export_error_title":"Export Error",
"error_files_export_error_message":"Could not export file links: {error}",
"export_options_dialog_title":"Export Options",
"export_options_description_label":"Choose the format for exporting error file links:",
"export_options_radio_link_only":"Link per line (URL only)",
"export_options_radio_link_only_tooltip":"Exports only the direct download URL for each failed file, one URL per line.",
"export_options_radio_with_details":"Export with details (URL [Post, File info])",
"export_options_radio_with_details_tooltip":"Exports the URL followed by details like Post Title, Post ID, and Original Filename in brackets.",
"export_options_export_button":"Export",

"no_errors_logged_title":"No Errors Logged",
"no_errors_logged_message":"No files were recorded as skipped due to errors in the last session or after retries.",

"progress_initializing_text":"Progress: Initializing...",
"progress_posts_text":"Progress: {processed_posts} / {total_posts} posts ({progress_percent:.1f}%)",
"progress_processing_post_text":"Progress: Processing post {processed_posts}...",
"progress_starting_text":"Progress: Starting...",
"downloading_file_known_size_text":"Downloading '{filename}' ({downloaded_mb:.1f}MB / {total_mb:.1f}MB)",
"downloading_file_unknown_size_text":"Downloading '{filename}' ({downloaded_mb:.1f}MB)",
"downloading_multipart_text":"DL '{filename}...': {downloaded_mb:.1f}/{total_mb:.1f} MB ({parts} parts @ {speed:.2f} MB/s)",
"downloading_multipart_initializing_text":"File: {filename} - Initializing parts...",
"status_completed":"Completed",
"status_cancelled_by_user":"Cancelled by user",
"files_downloaded_label":"downloaded",
"files_skipped_label":"skipped",
"retry_finished_text":"Retry Finished",
"succeeded_text":"Succeeded",
"empty_popup_button_tooltip_text":"Open Creator Selection (Browse creators.json)",
"failed_text":"Failed",
"ready_for_new_task_text":"Ready for new task."
,"fav_mode_active_label_text":"⭐ Favorite Mode is active. Please select filters below before choosing your favorite artists/posts. Select action below.",
"export_links_button_text":"Export Links",
"download_extracted_links_button_text":"Download",
"download_selected_button_text":"Download Selected",
"link_input_placeholder_text":"e.g., https://kemono.su/patreon/user/12345 or .../post/98765",
"link_input_tooltip_text":"Enter the full URL of a Kemono/Coomer creator's page or a specific post.\nExample (Creator): https://kemono.su/patreon/user/12345\nExample (Post): https://kemono.su/patreon/user/12345/post/98765",
"dir_input_placeholder_text":"Select folder where downloads will be saved",
"dir_input_tooltip_text":"Enter or browse to the main folder where all downloaded content will be saved.\nThis is required unless 'Only Links' mode is selected.",
"character_input_placeholder_text":"e.g., Tifa, Aerith, (Cloud, Zack)",
"custom_folder_input_placeholder_text":"Optional: Save this post to specific folder",
"custom_folder_input_tooltip_text":"If downloading a single post URL AND 'Separate Folders by Name/Title' is enabled,\nyou can enter a custom name here for that post's download folder.\nExample: My Favorite Scene",
"skip_words_input_placeholder_text":"e.g., WM, WIP, sketch, preview",
"remove_from_filename_input_placeholder_text":"e.g., patreon, HD",
"cookie_text_input_placeholder_no_file_selected_text":"Cookie string (if no cookies.txt selected)",
"cookie_text_input_placeholder_with_file_selected_text":"Using selected cookie file (see Browse...)",
"character_search_input_placeholder_text":"Search characters...",
"character_search_input_tooltip_text":"Type here to filter the list of known shows/characters below.",
"new_char_input_placeholder_text":"Add new show/character name",
"new_char_input_tooltip_text":"Enter a new show, game, or character name to add to the list above.",
"link_search_input_placeholder_text":"Search Links...",
"link_search_input_tooltip_text":"When in 'Only Links' mode, type here to filter the displayed links by text, URL, or platform.",
"manga_date_prefix_input_placeholder_text":"Prefix for Manga Filenames",
"manga_date_prefix_input_tooltip_text":"Optional prefix for 'Date Based' or 'Original File' manga filenames (e.g., 'Series Name').\nIf empty, files will be named based on the style without a prefix.",
"log_display_mode_links_view_text":"🔗 Links View",
"log_display_mode_progress_view_text":"⬇️ Progress View",
"download_external_links_dialog_title":"Download Selected External Links",
"select_all_button_text":"Select All",
"deselect_all_button_text":"Deselect All",
"cookie_browse_button_tooltip":"Browse for a cookie file (Netscape format, typically cookies.txt).\nThis will be used if 'Use Cookie' is checked and the text field above is empty."
,
"page_range_label_text":"Page Range:",
"start_page_input_placeholder":"Start",
"start_page_input_tooltip":"For creator URLs: Specify the starting page number to download from (e.g., 1, 2, 3).\nLeave blank or set to 1 to start from the first page.\nDisabled for single post URLs or Manga/Comic Mode.",
"page_range_to_label_text":"to",
"end_page_input_placeholder":"End",
"end_page_input_tooltip":"For creator URLs: Specify the ending page number to download up to (e.g., 5, 10).\nLeave blank to download all pages from the start page.\nDisabled for single post URLs or Manga/Comic Mode.",
"known_names_help_button_tooltip_text":"Open the application feature guide.",
"future_settings_button_tooltip_text":"Open application settings (Theme, Language, etc.).",
"link_search_button_tooltip_text":"Filter displayed links",
"confirm_add_all_dialog_title":"Confirm Adding New Names",
"confirm_add_all_info_label":"The following new names/groups from your 'Filter by Character(s)' input are not in 'Known.txt'.\nAdding them can improve folder organization for future downloads.\n\nReview the list and choose an action:",
"confirm_add_all_select_all_button":"Select All",
"confirm_add_all_deselect_all_button":"Deselect All",
"confirm_add_all_add_selected_button":"Add Selected to Known.txt",
"confirm_add_all_skip_adding_button":"Skip Adding These",
"confirm_add_all_cancel_download_button":"Cancel Download",
"cookie_help_dialog_title":"Cookie File Instructions",
"cookie_help_instruction_intro":"<p>To use cookies, you typically need a <b>cookies.txt</b> file from your browser.</p>",
"cookie_help_how_to_get_title":"<p><b>How to get cookies.txt:</b></p>",
"cookie_help_step1_extension_intro":"<li>Install the 'Get cookies.txt LOCALLY' extension for your Chrome-based browser:<br><a href=\"https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc\" style=\"color: #87CEEB;\">Get cookies.txt LOCALLY on Chrome Web Store</a></li>",
"cookie_help_step2_login":"<li>Go to the website (e.g., kemono.su or coomer.su) and log in if necessary.</li>",
"cookie_help_step3_click_icon":"<li>Click the extension's icon in your browser toolbar.</li>",
"cookie_help_step4_export":"<li>Click an 'Export' button (e.g., \"Export As\", \"Export cookies.txt\" - the exact wording might vary depending on the extension version).</li>",
"cookie_help_step5_save_file":"<li>Save the downloaded <code>cookies.txt</code> file to your computer.</li>",
"cookie_help_step6_app_intro":"<li>In this application:<ul>",
"cookie_help_step6a_checkbox":"<li>Ensure the 'Use Cookie' checkbox is checked.</li>",
"cookie_help_step6b_browse":"<li>Click the 'Browse...' button next to the cookie text field.</li>",
"cookie_help_step6c_select":"<li>Select the <code>cookies.txt</code> file you just saved.</li></ul></li>",
"cookie_help_alternative_paste":"<p>Alternatively, some extensions might allow you to copy the cookie string directly. If so, you can paste it into the text field instead of browsing for a file.</p>",
"cookie_help_proceed_without_button":"Download without Cookies",
"cookie_help_cancel_download_button":"Cancel Download",
"character_input_tooltip":(
"Enter character names (comma-separated). Supports advanced grouping and affects folder naming "
"if 'Separate Folders' is enabled.\n\n"
"Examples:\n"
"- Nami → Matches 'Nami', creates folder 'Nami'.\n"
"- (Ulti, Vivi) → Matches either, folder 'Ulti Vivi', adds both to Known.txt separately.\n"
"- (Boa, Hancock)~ → Matches either, folder 'Boa Hancock', adds as one group in Known.txt.\n\n"
"Names are treated as aliases for matching.\n\n"
"Filter Modes (button cycles):\n"
"- Files: Filters by filename.\n"
"- Title: Filters by post title.\n"
"- Both: Title first, then filename.\n"
"- Comments (Beta): Filename first, then post comments."
),
"tour_dialog_title":"Welcome to Kemono Downloader!",
"tour_dialog_never_show_checkbox":"Never show this tour again",
"tour_dialog_skip_button":"Skip Tour",
"tour_dialog_back_button":"Back",
"tour_dialog_next_button":"Next",
"tour_dialog_finish_button":"Finish",
"tour_dialog_step1_title":"👋 Welcome!",
"tour_dialog_step1_content":"""Hello! This quick tour will walk you through the main features of the Kemono Downloader, including recent updates like enhanced filtering, manga mode improvements, and cookie management.
        <ul>
        <li>My goal is to help you easily download content from <b>Kemono</b> and <b>Coomer</b>.</li><br>
        <li><b>🎨 Creator Selection Button:</b> Next to the URL input, click the palette icon to open a dialog. Browse and select creators from your <code>creators.json</code> file to quickly add their names to the URL input.</li><br>
        <li><b>Important Tip: App '(Not Responding)'?</b><br>
          After clicking 'Start Download', especially for large creator feeds or with many threads, the application might temporarily show as '(Not Responding)'. Your operating system (Windows, macOS, Linux) might even suggest you 'End Process' or 'Force Quit'.<br>
          <b>Please be patient!</b> The app is often still working hard in the background. Before force-closing, try checking your chosen 'Download Location' in your file explorer. If you see new folders being created or files appearing, it means the download is progressing correctly. Give it some time to become responsive again.</li><br>
        <li>Use the <b>Next</b> and <b>Back</b> buttons to navigate.</li><br>
        <li>Many options have tooltips if you hover over them for more details.</li><br>
        <li>Click <b>Skip Tour</b> to close this guide at any time.</li><br>        
        <li>Check <b>'Never show this tour again'</b> if you don't want to see this on future startups.</li>
        </ul>""",
"tour_dialog_step2_title":"① Getting Started",
"tour_dialog_step2_content":"""Let's start with the basics for downloading:
        <ul>
        <li><b>🔗 Kemono Creator/Post URL:</b><br>
          Paste the full web address (URL) of a creator's page (e.g., <i>https://kemono.su/patreon/user/12345</i>) 
        or a specific post (e.g., <i>.../post/98765</i>).</li><br>
          or a Coomer creator (e.g., <i>https://coomer.su/onlyfans/user/artistname</i>) 
        <li><b>📁 Download Location:</b><br>
          Click 'Browse...' to choose a folder on your computer where all downloaded files will be saved. 
        This is required unless you are using 'Only Links' mode.</li><br>
        <li><b>📄 Page Range (Creator URLs only):</b><br>
          If downloading from a creator's page, you can specify a range of pages to fetch (e.g., pages 2 to 5). 
        Leave blank for all pages. This is disabled for single post URLs or when <b>Manga/Comic Mode</b> is active.</li>
        </ul>""",
"tour_dialog_step3_title":"② Filtering Downloads",
"tour_dialog_step3_content":"""Refine what you download with these filters (most are disabled in 'Only Links' or 'Only Archives' modes):
        <ul>
        <li><b>🎯 Filter by Character(s):</b><br>
          Enter character names, comma-separated (e.g., <i>Tifa, Aerith</i>). Group aliases for a combined folder name: <i>(alias1, alias2, alias3)</i> becomes folder 'alias1 alias2 alias3' (after cleaning). All names in the group are used as aliases for matching.<br>
          The <b>'Filter: [Type]'</b> button (next to this input) cycles how this filter applies:
          <ul><li><i>Filter: Files:</i> Checks individual filenames. A post is kept if any file matches; only matching files are downloaded. Folder naming uses the character from the matching filename (if 'Separate Folders' is on).</li><br>
            <li><i>Filter: Title:</i> Checks post titles. All files from a matching post are downloaded. Folder naming uses the character from the matching post title.</li>
            <li><b>⤵️ Add to Filter Button (Known Names):</b> Next to the 'Add' button for Known Names (see Step 5), this opens a popup. Select names from your <code>Known.txt</code> list via checkboxes (with a search bar) to quickly add them to the 'Filter by Character(s)' field. Grouped names like <code>(Boa, Hancock)</code> from Known.txt will be added as <code>(Boa, Hancock)~</code> to the filter.</li><br>
            <li><i>Filter: Both:</i> Checks post title first. If it matches, all files are downloaded. If not, it then checks filenames, and only matching files are downloaded. Folder naming prioritizes title match, then file match.</li><br>
            <li><i>Filter: Comments (Beta):</i> Checks filenames first. If a file matches, all files from the post are downloaded. If no file match, it then checks post comments. If a comment matches, all files are downloaded. (Uses more API requests). Folder naming prioritizes file match, then comment match.</li></ul>
          This filter also influences folder naming if 'Separate Folders by Name/Title' is enabled.</li><br>
        <li><b>🚫 Skip with Words:</b><br>
          Enter words, comma-separated (e.g., <i>WIP, sketch, preview</i>). 
          The <b>'Scope: [Type]'</b> button (next to this input) cycles how this filter applies:
          <ul><li><i>Scope: Files:</i> Skips files if their names contain any of these words.</li><br>
            <li><i>Scope: Posts:</i> Skips entire posts if their titles contain any of these words.</li><br>
            <li><i>Scope: Both:</i> Applies both file and post title skipping (post first, then files).</li></ul></li><br>
        <li><b>Filter Files (Radio Buttons):</b> Choose what to download:
          <ul>
          <li><i>All:</i> Downloads all file types found.</li><br>
          <li><i>Images/GIFs:</i> Only common image formats and GIFs.</li><br>
          <li><i>Videos:</i> Only common video formats.</li><br>
          <li><b><i>📦 Only Archives:</i></b> Exclusively downloads <b>.zip</b> and <b>.rar</b> files. When selected, 'Skip .zip' and 'Skip .rar' checkboxes are automatically disabled and unchecked. 'Show External Links' is also disabled.</li><br>
          <li><i>🎧 Only Audio:</i> Only common audio formats (MP3, WAV, FLAC, etc.).</li><br>
          <li><i>🔗 Only Links:</i> Extracts and displays external links from post descriptions instead of downloading files. Download-related options and 'Show External Links' are disabled.</li>
          </ul></li>
        </ul>""",
"tour_dialog_step4_title":"③ Favorite Mode (Alternative Download)",
"tour_dialog_step4_content":"""The application offers a 'Favorite Mode' for downloading content from artists you've favorited on Kemono.su.
        <ul>
        <li><b>⭐ Favorite Mode Checkbox:</b><br>
          Located next to the '🔗 Only Links' radio button. Check this to activate Favorite Mode.</li><br>
        <li><b>What Happens in Favorite Mode:</b>
          <ul><li>The '🔗 Kemono Creator/Post URL' input area is replaced with a message indicating Favorite Mode is active.</li><br>
            <li>The standard 'Start Download', 'Pause', 'Cancel' buttons are replaced with '🖼️ Favorite Artists' and '📄 Favorite Posts' buttons (Note: 'Favorite Posts' is planned for the future).</li><br>
            <li>The '🍪 Use Cookie' option is automatically enabled and locked, as cookies are required to fetch your favorites.</li></ul></li><br>
        <li><b>🖼️ Favorite Artists Button:</b><br>
          Click this to open a dialog listing your favorited artists from Kemono.su. You can select one or more artists to download.</li><br>
        <li><b>Favorite Download Scope (Button):</b><br>
          This button (next to 'Favorite Posts') controls where selected favorites are downloaded:
          <ul><li><i>Scope: Selected Location:</i> All selected artists are downloaded into the main 'Download Location' you've set. Filters apply globally.</li><br>
            <li><i>Scope: Artist Folders:</i> A subfolder (named after the artist) is created inside your main 'Download Location' for each selected artist. Content for that artist goes into their specific subfolder. Filters apply within each artist's folder.</li></ul></li><br>
        <li><b>Filters in Favorite Mode:</b><br>
          The 'Filter by Character(s)', 'Skip with Words', and 'Filter Files' options still apply to the content downloaded from your selected favorite artists.</li>
        </ul>""",
"tour_dialog_step5_title":"④ Fine-Tuning Downloads",
"tour_dialog_step5_content":"""More options to customize your downloads:
        <ul>
        <li><b>Skip .zip / Skip .rar:</b> Check these to avoid downloading these archive file types. 
          <i>(Note: These are disabled and ignored if '📦 Only Archives' filter mode is selected).</i></li><br>
        <li><b>✂️ Remove Words from name:</b><br>
          Enter words, comma-separated (e.g., <i>patreon, [HD]</i>), to remove from downloaded filenames (case-insensitive).</li><br>
        <li><b>Download Thumbnails Only:</b> Downloads small preview images instead of full-sized files (if available).</li><br>
        <li><b>Compress Large Images:</b> If the 'Pillow' library is installed, images larger than 1.5MB will be converted to WebP format if the WebP version is significantly smaller.</li><br>
        <li><b>🗄️ Custom Folder Name (Single Post Only):</b><br>
          If you are downloading a single specific post URL AND 'Separate Folders by Name/Title' is enabled, 
        you can enter a custom name here for that post's download folder.</li><br>
        <li><b>🍪 Use Cookie:</b> Check this to use cookies for requests. You can either:
          <ul><li>Enter a cookie string directly into the text field (e.g., <i>name1=value1; name2=value2</i>).</li><br>
            <li>Click 'Browse...' to select a <i>cookies.txt</i> file (Netscape format). The path will appear in the text field.</li></ul>
          This is useful for accessing content that requires login. The text field takes precedence if filled. 
        If 'Use Cookie' is checked but both the text field and browsed file are empty, it will try to load 'cookies.txt' from the app's directory.</li>
        </ul>""",
"tour_dialog_step6_title":"⑤ Organization & Performance",
"tour_dialog_step6_content":"""Organize your downloads and manage performance:
        <ul>
        <li><b>⚙️ Separate Folders by Name/Title:</b> Creates subfolders based on the 'Filter by Character(s)' input or post titles (can use the <b>Known.txt</b> list as a fallback for folder names).</li><br>
        <li><b>Subfolder per Post:</b> If 'Separate Folders' is on, this creates an additional subfolder for <i>each individual post</i> inside the main character/title folder.</li><br>
        <li><b>🚀 Use Multithreading (Threads):</b> Enables faster operations. The number in 'Threads' input means:
          <ul><li>For <b>Creator Feeds:</b> Number of posts to process simultaneously. Files within each post are downloaded sequentially by its worker (unless 'Date Based' manga naming is on, which forces 1 post worker).</li><br>
            <li>For <b>Single Post URLs:</b> Number of files to download concurrently from that single post.</li></ul>
          If unchecked, 1 thread is used. High thread counts (e.g., >40) may show an advisory.</li><br>
        <li><b>Multi-part Download Toggle (Top-right of log area):</b><br>
          The <b>'Multi-part: [ON/OFF]'</b> button allows enabling/disabling multi-segment downloads for individual large files. 
          <ul><li><b>ON:</b> Can speed up large file downloads (e.g., videos) but may increase UI choppiness or log spam with many small files. An advisory will appear when enabling. If a multi-part download fails, it retries as single-stream.</li><br>
            <li><b>OFF (Default):</b> Files are downloaded in a single stream.</li></ul>
          This is disabled if 'Only Links' or 'Only Archives' mode is active.</li><br>
        <li><b>📖 Manga/Comic Mode (Creator URLs only):</b> Tailored for sequential content.
          <ul>
          <li>Downloads posts from <b>oldest to newest</b>.</li><br>
          <li>The 'Page Range' input is disabled as all posts are fetched.</li><br>
          <li>A <b>filename style toggle button</b> (e.g., 'Name: Post Title') appears in the top-right of the log area when this mode is active for a creator feed. Click it to cycle through naming styles:
            <ul>
            <li><b><i>Name: Post Title (Default):</i></b> The first file in a post is named after the post's cleaned title (e.g., 'My Chapter 1.jpg'). Subsequent files within the *same post* will attempt to keep their original filenames (e.g., 'page_02.png', 'bonus_art.jpg'). If the post has only one file, it's named after the post title. This is generally recommended for most manga/comics.</li><br>
            <li><b><i>Name: Original File:</i></b> All files attempt to keep their original filenames. An optional prefix (e.g., 'MySeries_') can be entered in the input field that appears next to the style button. Example: 'MySeries_OriginalFile.jpg'.</li><br>
            <li><b><i>Name: Title+G.Num (Post Title + Global Numbering):</i></b> All files across all posts in the current download session are named sequentially using the post's cleaned title as a prefix, followed by a global counter. For example: Post 'Chapter 1' (2 files) -> 'Chapter 1_001.jpg', 'Chapter 1_002.png'. The next post, 'Chapter 2' (1 file), would continue the numbering -> 'Chapter 2_003.jpg'. Multithreading for post processing is automatically disabled for this style to ensure correct global numbering.</li><br>
            <li><b><i>Name: Date Based:</i></b> Files are named sequentially (001.ext, 002.ext, ...) based on post publication order. An optional prefix (e.g., 'MySeries_') can be entered in the input field that appears next to the style button. Example: 'MySeries_001.jpg'. Multithreading for post processing is automatically disabled for this style.</li>
            </ul>
          </li><br>
          <li>For best results with 'Name: Post Title', 'Name: Title+G.Num', or 'Name: Date Based' styles, use the 'Filter by Character(s)' field with the manga/series title for folder organization.</li>
          </ul></li><br>
        <li><b>🎭 Known.txt for Smart Folder Organization:</b><br>
          <code>Known.txt</code> (in the app's directory) allows fine-grained control over automatic folder organization when 'Separate Folders by Name/Title' is active.
          <ul>
            <li><b>How it Works:</b> Each line in <code>Known.txt</code> is an entry. 
              <ul><li>A simple line like <code>My Awesome Series</code> means content matching this will go into a folder named "My Awesome Series".</li><br>
                <li>A grouped line like <code>(Character A, Char A, Alt Name A)</code> means content matching "Character A", "Char A", OR "Alt Name A" will ALL go into a single folder named "Character A Char A Alt Name A" (after cleaning). All terms in the parentheses become aliases for that folder.</li></ul></li>
            <li><b>Intelligent Fallback:</b> When 'Separate Folders by Name/Title' is active, and if a post doesn't match any specific 'Filter by Character(s)' input, the downloader consults <code>Known.txt</code> to find a matching primary name for folder creation.</li><br>
            <li><b>User-Friendly Management:</b> Add simple (non-grouped) names via the UI list below. For advanced editing (like creating/modifying grouped aliases), click <b>'Open Known.txt'</b> to edit the file in your text editor. The app reloads it on next use or startup.</li>
          </ul>
        </li>
        </ul>""",
"tour_dialog_step7_title":"⑥ Common Errors & Troubleshooting",
"tour_dialog_step7_content":"""Sometimes, downloads might encounter issues. Here are a few common ones:
        <ul>
        <li><b>Character Input Tooltip:</b><br>
          Enter character names, comma-separated (e.g., <i>Tifa, Aerith</i>).<br>
          Group aliases for a combined folder name: <i>(alias1, alias2, alias3)</i> becomes folder 'alias1 alias2 alias3'.<br>
          All names in the group are used as aliases for matching content.<br><br>
          The 'Filter: [Type]' button next to this input cycles how this filter applies:<br>
          - Filter: Files: Checks individual filenames. Only matching files are downloaded.<br>
          - Filter: Title: Checks post titles. All files from a matching post are downloaded.<br>
          - Filter: Both: Checks post title first. If no match, then checks filenames.<br>
          - Filter: Comments (Beta): Checks filenames first. If no match, then checks post comments.<br><br>
          This filter also influences folder naming if 'Separate Folders by Name/Title' is enabled.</li><br>      
        <li><b>502 Bad Gateway / 503 Service Unavailable / 504 Gateway Timeout:</b><br>
          These usually indicate temporary server-side problems with Kemono/Coomer. The site might be overloaded, down for maintenance, or experiencing issues. <br>
          <b>Solution:</b> Wait a while (e.g., 30 minutes to a few hours) and try again later. Check the site directly in your browser.</li><br>
        <li><b>Connection Lost / Connection Refused / Timeout (during file download):</b><br>
          This can happen due to your internet connection, server instability, or if the server drops the connection for a large file. <br>
          <b>Solution:</b> Check your internet. Try reducing the number of 'Threads' if it's high. The app might prompt to retry some failed files at the end of a session.</li><br>
        <li><b>IncompleteRead Error:</b><br>
          The server sent less data than expected. Often a temporary network hiccup or server issue. <br>
          <b>Solution:</b> The app will often mark these files for a retry attempt at the end of the download session.</li><br>
        <li><b>403 Forbidden / 401 Unauthorized (less common for public posts):</b><br>
          You might not have permission to access the content. For some paywalled or private content, using the 'Use Cookie' option with valid cookies from your browser session might help. Ensure your cookies are fresh.</li><br>
        <li><b>404 Not Found:</b><br>
          The post or file URL is incorrect, or the content has been removed from the site. Double-check the URL.</li><br>
        <li><b>'No posts found' / 'Target post not found':</b><br>
          Ensure the URL is correct and the creator/post exists. If using page ranges, make sure they are valid for the creator. For very new posts, there might be a slight delay before they appear in the API.</li><br>
        <li><b>General Slowness / App '(Not Responding)':</b><br>
          As mentioned in Step 1, if the app seems to hang after starting, especially with large creator feeds or many threads, please give it time. It's likely processing data in the background. Reducing thread count can sometimes improve responsiveness if this is frequent.</li>
        </ul>""",
"tour_dialog_step8_title":"⑦ Logs & Final Controls",
"tour_dialog_step8_content":"""Monitoring and Controls:
        <ul>
        <li><b>📜 Progress Log / Extracted Links Log:</b> Shows detailed download messages. If '🔗 Only Links' mode is active, this area displays the extracted links.</li><br>
        <li><b>Show External Links in Log:</b> If checked, a secondary log panel appears below the main log to display any external links found in post descriptions. <i>(This is disabled if '🔗 Only Links' or '📦 Only Archives' mode is active).</i></li><br>
        <li><b>Log View Toggle (👁️ / 🙈 Button):</b><br>
          This button (top-right of log area) switches the main log view:
          <ul><li><b>👁️ Progress Log (Default):</b> Shows all download activity, errors, and summaries.</li><br>
            <li><b>🙈 Missed Character Log:</b> Displays a list of key terms from post titles that were skipped due to your 'Filter by Character(s)' settings. Useful for identifying content you might be unintentionally missing.</li></ul></li><br>
        <li><b>🔄 Reset:</b> Clears all input fields, logs, and resets temporary settings to their defaults. Can only be used when no download is active.</li><br>
        <li><b>⬇️ Start Download / 🔗 Extract Links / ⏸️ Pause / ❌ Cancel:</b> These buttons control the process. 'Cancel & Reset UI' stops the current operation and performs a soft UI reset, preserving your URL and Directory inputs. 'Pause/Resume' allows temporarily halting and continuing.</li><br>
        <li>If some files fail with recoverable errors (like 'IncompleteRead'), you might be prompted to retry them at the end of a session.</li>
        </ul>
        <br>You're all set! Click <b>'Finish'</b> to close the tour and start using the downloader."""
},
"ja":{
"settings_dialog_title":"設定",
"language_label":"言語:",
"lang_english":"英語",
"lang_japanese":"日本語",
"theme_toggle_light":"ライトモードに切り替え",
"theme_toggle_dark":"ダークモードに切り替え",
"theme_tooltip_light":"アプリケーションの外観を明るく変更します。",
"theme_tooltip_dark":"アプリケーションの外観を暗く変更します。",
"ok_button":"OK",
"appearance_group_title":"外観",
"language_group_title":"言語設定",
"creator_post_url_label":"🔗 Kemonoクリエイター/投稿URL:",
"download_location_label":"📁 ダウンロード場所:",
"filter_by_character_label":"🎯 キャラクターでフィルタリング (コンマ区切り):",
"skip_with_words_label":"🚫 スキップする単語 (コンマ区切り):",
"remove_words_from_name_label":"✂️ 名前から単語を削除:",
"filter_all_radio":"すべて",
"filter_images_radio":"画像/GIF",
"filter_videos_radio":"動画",
"filter_archives_radio":"📦 アーカイブのみ",
"filter_links_radio":"🔗 リンクのみ",
"filter_audio_radio":"🎧 音声のみ",
"favorite_mode_checkbox_label":"⭐ お気に入りモード",
"browse_button_text":"参照...",
"char_filter_scope_files_text":"フィルター: ファイル",
"char_filter_scope_files_tooltip":"現在のスコープ: ファイル\n\nファイル名で個々のファイルをフィルターします。いずれかのファイルが一致すれば投稿は保持されます。\nその投稿から一致するファイルのみがダウンロードされます。\n例: フィルター「ティファ」。ファイル「ティファ_アートワーク.jpg」が一致し、ダウンロードされます。\nフォルダー命名: 一致するファイル名のキャラクターを使用します。\n\nクリックして次に循環: 両方",
"char_filter_scope_title_text":"フィルター: タイトル",
"char_filter_scope_title_tooltip":"現在のスコープ: タイトル\n\n投稿タイトルで投稿全体をフィルターします。一致する投稿のすべてのファイルがダウンロードされます。\n例: フィルター「エアリス」。タイトル「エアリスの庭」の投稿が一致し、すべてのファイルがダウンロードされます。\nフォルダー命名: 一致する投稿タイトルのキャラクターを使用します。\n\nクリックして次に循環: ファイル",
"char_filter_scope_both_text":"フィルター: 両方",
"char_filter_scope_both_tooltip":"現在のスコープ: 両方 (タイトル、次にファイル)\n\n1. 投稿タイトルを確認: 一致する場合、投稿のすべてのファイルがダウンロードされます。\n2. タイトルが一致しない場合、ファイル名を確認: いずれかのファイルが一致する場合、そのファイルのみがダウンロードされます。\n例: フィルター「クラウド」。\n - 投稿「クラウド・ストライフ」(タイトル一致) -> すべてのファイルがダウンロードされます。\n - 投稿「バイクチェイス」と「クラウド_フェンリル.jpg」(ファイル一致) -> 「クラウド_フェンリル.jpg」のみがダウンロードされます。\nフォルダー命名: タイトル一致を優先し、次にファイル一致を優先します。\n\nクリックして次に循環: コメント",
"char_filter_scope_comments_text":"フィルター: コメント (ベータ)",
"char_filter_scope_comments_tooltip":"現在のスコープ: コメント (ベータ - ファイル優先、次にコメントをフォールバック)\n\n1. ファイル名を確認: 投稿内のいずれかのファイルがフィルターに一致する場合、投稿全体がダウンロードされます。このフィルター用語についてはコメントはチェックされません。\n2. ファイルが一致しない場合、次に投稿コメントを確認: コメントが一致する場合、投稿全体がダウンロードされます。\n例: フィルター「バレット」。\n - 投稿A: ファイル「バレット_ガンアーム.jpg」、「other.png」。ファイル「バレット_ガンアーム.jpg」が一致。投稿Aのすべてのファイルがダウンロードされます。「バレット」についてはコメントはチェックされません。\n - 投稿B: ファイル「ダイン.jpg」、「ウェポン.gif」。コメント: 「...バレット・ウォーレスの絵...」。「バレット」にファイル一致なし。コメントが一致。投稿Bのすべてのファイルがダウンロードされます。\nフォルダー命名: ファイル一致のキャラクターを優先し、次にコメント一致のキャラクターを優先します。\n\nクリックして次に循環: タイトル",
"char_filter_scope_unknown_text":"フィルター: 不明",
"char_filter_scope_unknown_tooltip":"現在のスコープ: 不明\n\nキャラクターフィルタースコープが不明な状態です。循環またはリセットしてください。\n\nクリックして次に循環: タイトル",
"skip_words_input_tooltip":(
"特定のコンテンツのダウンロードをスキップするために、単語をカンマ区切りで入力します（例: WIP, sketch, preview）。\n\n"
"この入力の隣にある「スコープ: [タイプ]」ボタンは、このフィルターの適用方法を循環します:\n"
"- スコープ: ファイル: 名前にこれらの単語のいずれかを含む場合、個々のファイルをスキップします。\n"
"- スコープ: 投稿: タイトルにこれらの単語のいずれかを含む場合、投稿全体をスキップします。\n"
"- スコープ: 両方: 両方を適用します（まず投稿タイトル、次に投稿タイトルがOKな場合は個々のファイル）。"
),
"remove_words_input_tooltip":(
"ダウンロードしたファイル名から削除する単語をカンマ区切りで入力します（大文字・小文字を区別しません）。\n"
"一般的な接頭辞や接尾辞を整理するのに役立ちます。\n"
"例: patreon, kemono, [HD], _final"
),
"skip_scope_files_text":"スコープ: ファイル",
"skip_scope_files_tooltip":"現在のスキップスコープ: ファイル\n\n「スキップする単語」のいずれかを含む場合、個々のファイルをスキップします。\n例: スキップする単語「WIP、スケッチ」。\n- ファイル「art_WIP.jpg」-> スキップ。\n- ファイル「final_art.png」-> ダウンロード (他の条件が満たされた場合)。\n\n投稿は他のスキップされないファイルについて引き続き処理されます。\nクリックして次に循環: 両方",
"skip_scope_posts_text":"スコープ: 投稿",
"skip_scope_posts_tooltip":"現在のスキップスコープ: 投稿\n\n「スキップする単語」のいずれかを含む場合、投稿全体をスキップします。\nスキップされた投稿のすべてのファイルは無視されます。\n例: スキップする単語「プレビュー、お知らせ」。\n- 投稿「エキサイティングなお知らせ！」-> スキップ。\n- 投稿「完成したアートワーク」-> 処理 (他の条件が満たされた場合)。\n\nクリックして次に循環: ファイル",
"skip_scope_both_text":"スコープ: 両方",
"skip_scope_both_tooltip":"現在のスキップスコープ: 両方 (投稿、次にファイル)\n\n1. 投稿タイトルを確認: タイトルにスキップワードが含まれている場合、投稿全体がスキップされます。\n2. 投稿タイトルがOKの場合、次に個々のファイル名を確認: ファイル名にスキップワードが含まれている場合、そのファイルのみがスキップされます。\n例: スキップする単語「WIP、スケッチ」。\n- 投稿「スケッチとWIP」(タイトル一致) -> 投稿全体がスキップされます。\n- 投稿「アートアップデート」(タイトルOK) とファイル:\n    - 「キャラクター_WIP.jpg」(ファイル一致) -> スキップ。\n    - 「最終シーン.png」(ファイルOK) -> ダウンロード。\n\nクリックして次に循環: 投稿",
"skip_scope_unknown_text":"スコープ: 不明",
"skip_scope_unknown_tooltip":"現在のスキップスコープ: 不明\n\nスキップワードスコープが不明な状態です。循環またはリセットしてください。\n\nクリックして次に循環: 投稿",
"language_change_title":"言語が変更されました",
"language_change_message":"言語が変更されました。すべての変更を完全に有効にするには、再起動が必要です。",
"language_change_informative":"今すぐアプリケーションを再起動しますか？",
"restart_now_button":"今すぐ再起動",
"skip_zip_checkbox_label":".zipをスキップ",
"skip_rar_checkbox_label":".rarをスキップ",
"download_thumbnails_checkbox_label":"サムネイルのみダウンロード",
"scan_content_images_checkbox_label":"コンテンツ内の画像をスキャン",
"compress_images_checkbox_label":"WebPに圧縮",
"separate_folders_checkbox_label":"名前/タイトルでフォルダを分ける",
"subfolder_per_post_checkbox_label":"投稿ごとにサブフォルダ",
"use_cookie_checkbox_label":"Cookieを使用",
"use_multithreading_checkbox_base_label":"マルチスレッドを使用",
"show_external_links_checkbox_label":"ログに外部リンクを表示",
"manga_comic_mode_checkbox_label":"マンガ/コミックモード",
"threads_label":"スレッド数:",
"start_download_button_text":"⬇️ ダウンロード開始",
"start_download_button_tooltip":"現在の設定でダウンロードまたはリンク抽出プロセスを開始します。",
"extract_links_button_text":"🔗 リンクを抽出",
"pause_download_button_text":"⏸️ 一時停止",
"pause_download_button_tooltip":"進行中のダウンロードプロセスを一時停止します。",
"resume_download_button_text":"▶️ 再開",
"resume_download_button_tooltip":"ダウンロードを再開します。",
"cancel_button_text":"❌ 中止してUIリセット",
"cancel_button_tooltip":"進行中のダウンロード/抽出プロセスを中止し、UIフィールドをリセットします（URLとディレクトリは保持）。",
"error_button_text":"エラー",
"error_button_tooltip":"エラーによりスキップされたファイルを表示し、オプションで再試行します。",
"cancel_retry_button_text":"❌ 再試行を中止",
"known_chars_label_text":"🎭 既知の番組/キャラクター (フォルダ名用):",
"open_known_txt_button_text":"Known.txtを開く",
"known_chars_list_tooltip":"このリストには、「フォルダを分ける」がオンで、特定の「キャラクターでフィルタリング」が提供されていないか、投稿に一致しない場合に、自動フォルダ作成に使用される名前が含まれています。\n頻繁にダウンロードするシリーズ、ゲーム、またはキャラクターの名前を追加してください。",
"open_known_txt_button_tooltip":"デフォルトのテキストエディタで「Known.txt」ファイルを開きます。\nファイルはアプリケーションのディレクトリにあります。",
"add_char_button_text":"➕ 追加",
"add_char_button_tooltip":"入力フィールドの名前を「既知の番組/キャラクター」リストに追加します。",
"add_to_filter_button_text":"⤵️ フィルターに追加",
"add_to_filter_button_tooltip":"「既知の番組/キャラクター」リストから名前を選択して、上の「キャラクターでフィルタリング」フィールドに追加します。",
"delete_char_button_text":"🗑️ 選択項目を削除",
"delete_char_button_tooltip":"選択した名前を「既知の番組/キャラクター」リストから削除します。",
"radio_all_tooltip":"投稿で見つかったすべてのファイルタイプをダウンロードします。",
"radio_images_tooltip":"一般的な画像形式（JPG、PNG、GIF、WEBPなど）のみをダウンロードします。",
"radio_videos_tooltip":"一般的な動画形式（MP4、MKV、WEBM、MOVなど）のみをダウンロードします。",
"radio_only_archives_tooltip":".zipおよび.rarファイルのみを排他的にダウンロードします。他のファイル固有のオプションは無効になります。",
"radio_only_audio_tooltip":"一般的な音声形式（MP3、WAV、FLACなど）のみをダウンロードします。",
"radio_only_links_tooltip":"ファイルをダウンロードする代わりに、投稿の説明から外部リンクを抽出して表示します。\nダウンロード関連のオプションは無効になります。",
"favorite_mode_checkbox_tooltip":"お気に入りモードを有効にして、保存したアーティスト/投稿を閲覧します。\nこれにより、URL入力がお気に入り選択ボタンに置き換えられます。",
"skip_zip_checkbox_tooltip":"チェックすると、.zipアーカイブファイルはダウンロードされません。\n（「アーカイブのみ」が選択されている場合は無効）。",
"skip_rar_checkbox_tooltip":"チェックすると、.rarアーカイブファイルはダウンロードされません。\n（「アーカイブのみ」が選択されている場合は無効）。",
"download_thumbnails_checkbox_tooltip":"フルサイズのファイルの代わりにAPIから小さなプレビュー画像をダウンロードします（利用可能な場合）。\n「コンテンツ内の画像をスキャン」もチェックされている場合、このモードではコンテンツスキャンで見つかった画像のみがダウンロードされます（APIサムネイルは無視）。",
"scan_content_images_checkbox_tooltip":"チェックすると、ダウンローダーは投稿のHTMLコンテンツをスキャンして画像URL（<img>タグまたは直接リンクから）を探します。\nこれには、<img>タグの相対パスを完全なURLに解決することも含まれます。\n<img>タグの相対パス（例: /data/image.jpg）は完全なURLに解決されます。\n画像が投稿の説明にあるがAPIのファイル/添付ファイルリストにない場合に便利です。",
"compress_images_checkbox_tooltip":"1.5MBを超える画像をWebP形式に圧縮します（Pillowが必要）。",
"use_subfolders_checkbox_tooltip":"「キャラクターでフィルタリング」入力または投稿タイトルに基づいてサブフォルダを作成します。\n特定のフィルターが投稿に一致しない場合、フォルダ名のフォールバックとして「既知の番組/キャラクター」リストを使用します。\n単一投稿の「キャラクターでフィルタリング」入力と「カスタムフォルダ名」を有効にします。",
"use_subfolder_per_post_checkbox_tooltip":"投稿ごとにサブフォルダを作成します。「フォルダを分ける」もオンの場合、キャラクター/タイトルフォルダ内に作成されます。",
"use_cookie_checkbox_tooltip":"チェックすると、リクエストにアプリケーションディレクトリの「cookies.txt」（Netscape形式）のCookieを使用しようとします。\nKemono/Coomerでログインが必要なコンテンツにアクセスするのに便利です。",
"cookie_text_input_tooltip":"Cookie文字列を直接入力します。\n「Cookieを使用」がチェックされていて、「cookies.txt」が見つからないか、このフィールドが空でない場合に使用されます。\n形式はバックエンドがどのように解析するかに依存します（例: 「name1=value1; name2=value2」）。",
"use_multithreading_checkbox_tooltip":"同時操作を有効にします。詳細については、「スレッド数」入力を参照してください。",
"thread_count_input_tooltip":(
"同時操作の数。\n- 単一投稿: 同時ファイルダウンロード数（1～10推奨）。\n"
"- クリエイターフィードURL: 同時に処理する投稿数（1～200推奨）。\n"
"  各投稿内のファイルはそのワーカーによって1つずつダウンロードされます。\n「マルチスレッドを使用」がオフの場合、1スレッドが使用されます。"),
"external_links_checkbox_tooltip":"チェックすると、メインログの下にセカンダリログパネルが表示され、投稿の説明で見つかった外部リンクが表示されます。\n（「リンクのみ」または「アーカイブのみ」モードがアクティブな場合は無効）。",
"manga_mode_checkbox_tooltip":"投稿を古いものから新しいものへダウンロードし、ファイル名を投稿タイトルに基づいて変更します（クリエイターフィードのみ）。",
"progress_log_label_text":"📜 進捗ログ:",
"multipart_on_button_text":"マルチパート: オン",
"multipart_on_button_tooltip":"マルチパートダウンロード: オン\n\n大きなファイルを複数のセグメントで同時にダウンロードします。\n- 単一の大きなファイル（例: 動画）のダウンロードを高速化できます。\n- CPU/ネットワーク使用量が増加する可能性があります。\n- 多くの小さなファイルがあるフィードでは、速度の利点はなく、UI/ログが煩雑になることがあります。\n- マルチパートが失敗した場合、シングルストリームで再試行します。\n\nクリックしてオフにします。",
"multipart_off_button_text":"マルチパート: オフ",
"multipart_off_button_tooltip":"マルチパートダウンロード: オフ\n\nすべてのファイルが単一のストリームを使用してダウンロードされます。\n- 安定しており、ほとんどのシナリオ、特に多くの小さなファイルに適しています。\n- 大きなファイルは連続してダウンロードされます。\n\nクリックしてオンにします（アドバイザリを参照）。",
"reset_button_text":"🔄 リセット",
"reset_button_tooltip":"すべての入力とログをデフォルト状態にリセットします（アイドル時のみ）。",
"progress_idle_text":"進捗: アイドル",
"missed_character_log_label_text":"🚫 見逃したキャラクターログ:",
"creator_popup_title":"クリエイター選択",
"creator_popup_search_placeholder":"名前、サービスで検索、またはクリエイターURLを貼り付け...",
"creator_popup_add_selected_button":"選択項目を追加",
"creator_popup_scope_characters_button":"スコープ: キャラクター",
"creator_popup_scope_creators_button":"スコープ: クリエイター",
"favorite_artists_button_text":"🖼️ お気に入りアーティスト",
"favorite_artists_button_tooltip":"Kemono.su/Coomer.suでお気に入りのアーティストを閲覧してダウンロードします。",
"favorite_posts_button_text":"📄 お気に入り投稿",
"favorite_posts_button_tooltip":"Kemono.su/Coomer.suでお気に入りの投稿を閲覧してダウンロードします。",
"favorite_scope_selected_location_text":"スコープ: 選択場所",
"favorite_scope_selected_location_tooltip":"現在のお気に入りダウンロードスコープ: 選択場所\n\n選択したすべてのお気に入りアーティスト/投稿は、UIで指定されたメインの「ダウンロード場所」にダウンロードされます。\nフィルター（キャラクター、スキップワード、ファイルタイプ）は、これらのアーティストのすべてのコンテンツにグローバルに適用されます。\n\nクリックして変更: アーティストフォルダ",
"favorite_scope_artist_folders_text":"スコープ: アーティストフォルダ",
"favorite_scope_artist_folders_tooltip":"現在のお気に入りダウンロードスコープ: アーティストフォルダ\n\n選択した各お気に入りアーティスト/投稿に対して、メインの「ダウンロード場所」内に新しいサブフォルダ（アーティスト名）が作成されます。\nそのアーティスト/投稿のコンテンツは、特定のサブフォルダにダウンロードされます。\nフィルター（キャラクター、スキップワード、ファイルタイプ）は、各アーティストのフォルダ内で適用されます。\n\nクリックして変更: 選択場所",
"favorite_scope_unknown_text":"スコープ: 不明",
"favorite_scope_unknown_tooltip":"お気に入りのダウンロードスコープが不明です。クリックして循環します。",
"manga_style_post_title_text":"名前: 投稿タイトル",
"manga_style_original_file_text":"名前: 元ファイル名",
"manga_style_date_based_text":"名前: 日付順",
"manga_style_title_global_num_text":"名前: タイトル+通し番号",
"manga_style_unknown_text":"名前: 不明なスタイル",
"fav_artists_dialog_title":"お気に入りアーティスト",
"fav_artists_loading_status":"お気に入りアーティストを読み込み中...",
"fav_artists_search_placeholder":"アーティストを検索...",
"fav_artists_select_all_button":"すべて選択",
"fav_artists_deselect_all_button":"すべて選択解除",
"fav_artists_download_selected_button":"選択項目をダウンロード",
"fav_artists_cancel_button":"キャンセル",
"fav_artists_loading_from_source_status":"⏳ {source_name} からお気に入りを読み込み中...",
"fav_artists_found_status":"{count} 人のお気に入りアーティストが見つかりました。",
"fav_artists_none_found_status":"Kemono.suまたはCoomer.suにお気に入りアーティストが見つかりません。",
"fav_artists_failed_status":"お気に入りの取得に失敗しました。",
"fav_artists_cookies_required_status":"エラー: Cookieが有効ですが、どのソースからも読み込めませんでした。",
"fav_artists_no_favorites_after_processing":"処理後にお気に入りアーティストが見つかりませんでした。",
"fav_artists_no_selection_title":"選択なし",
"fav_artists_no_selection_message":"ダウンロードするアーティストを少なくとも1人選択してください。",

"fav_posts_dialog_title":"お気に入り投稿",
"fav_posts_loading_status":"お気に入り投稿を読み込み中...",
"fav_posts_search_placeholder":"投稿を検索 (タイトル、クリエイター、ID、サービス)...",
"fav_posts_select_all_button":"すべて選択",
"fav_posts_deselect_all_button":"すべて選択解除",
"fav_posts_download_selected_button":"選択項目をダウンロード",
"fav_posts_cancel_button":"キャンセル",
"fav_posts_cookies_required_error":"エラー: お気に入り投稿にはCookieが必要ですが、読み込めませんでした。",
"fav_posts_auth_failed_title":"認証失敗 (投稿)",
"fav_posts_auth_failed_message":"認証エラーのため、お気に入り{domain_specific_part}を取得できませんでした:\n\n{error_message}\n\nこれは通常、サイトのCookieがないか、無効であるか、期限切れであることを意味します。Cookieの設定を確認してください。",
"fav_posts_fetch_error_title":"取得エラー",
"fav_posts_fetch_error_message":"{domain}からのお気に入り取得エラー{error_message_part}",
"fav_posts_no_posts_found_status":"お気に入り投稿が見つかりません。",
"fav_posts_found_status":"{count}件のお気に入り投稿が見つかりました。",
"fav_posts_display_error_status":"投稿の表示エラー: {error}",
"fav_posts_ui_error_title":"UIエラー",
"fav_posts_ui_error_message":"お気に入り投稿を表示できませんでした: {error}",
"fav_posts_auth_failed_message_generic":"認証エラーのため、お気に入り{domain_specific_part}を取得できませんでした。これは通常、サイトのCookieがないか、無効であるか、期限切れであることを意味します。Cookieの設定を確認してください。",
"key_fetching_fav_post_list_init":"お気に入り投稿リストを取得中...", # JA_ADD_KEY_HERE
"empty_popup_button_tooltip_text": "クリエイター選択を開く (creators.json を参照)",
"key_fetching_from_source_kemono_su":"Kemono.suからお気に入りを取得中...",
"key_fetching_from_source_coomer_su":"Coomer.suからお気に入りを取得中...",
"fav_posts_fetch_cancelled_status":"お気に入り投稿の取得がキャンセルされました。",

"known_names_filter_dialog_title":"既知の名前をフィルターに追加",
"known_names_filter_search_placeholder":"名前を検索...",
"known_names_filter_select_all_button":"すべて選択",
"known_names_filter_deselect_all_button":"すべて選択解除",
"known_names_filter_add_selected_button":"選択項目を追加",

"error_files_dialog_title":"エラーによりスキップされたファイル",
"error_files_no_errors_label":"前回のセッションまたは再試行後にエラーでスキップされたと記録されたファイルはありません。",
"error_files_found_label":"以下の{count}個のファイルがダウンロードエラーによりスキップされました:",
"error_files_select_all_button":"すべて選択",
"error_files_retry_selected_button":"選択項目を再試行",
"error_files_export_urls_button":"URLを.txtにエクスポート",
"error_files_no_selection_retry_message":"再試行するファイルを少なくとも1つ選択してください。",
"error_files_no_errors_export_title":"エラーなし",
"error_files_no_errors_export_message":"エクスポートするエラーファイルのURLはありません。",
"error_files_no_urls_found_export_title":"URLが見つかりません",
"error_files_no_urls_found_export_message":"エラーファイルリストからエクスポートするURLを抽出できませんでした。",
"error_files_save_dialog_title":"エラーファイルのURLを保存",
"error_files_export_success_title":"エクスポート成功",
"error_files_export_success_message":"{count}件のエントリを正常にエクスポートしました:\n{filepath}",
"error_files_export_error_title":"エクスポートエラー",
"error_files_export_error_message":"ファイルリンクをエクスポートできませんでした: {error}",
"export_options_dialog_title":"エクスポートオプション",
"export_options_description_label":"エラーファイルリンクのエクスポート形式を選択してください:",
"export_options_radio_link_only":"1行に1リンク (URLのみ)",
"export_options_radio_link_only_tooltip":"失敗した各ファイルの直接ダウンロードURLのみを1行に1URLずつエクスポートします。",
"export_options_radio_with_details":"詳細付きでエクスポート (URL [投稿、ファイル情報])",
"export_options_radio_with_details_tooltip":"URLの後に投稿タイトル、投稿ID、元のファイル名などの詳細を角括弧で囲んでエクスポートします。",
"export_options_export_button":"エクスポート",

"no_errors_logged_title":"エラー記録なし",
"no_errors_logged_message":"前回のセッションまたは再試行後にエラーでスキップされたと記録されたファイルはありません。",

"progress_initializing_text":"進捗: 初期化中...",
"progress_posts_text":"進捗: {processed_posts} / {total_posts} 件の投稿 ({progress_percent:.1f}%)",
"progress_processing_post_text":"進捗: 投稿 {processed_posts} を処理中...",
"progress_starting_text":"進捗: 開始中...",
"downloading_file_known_size_text":"'{filename}' をダウンロード中 ({downloaded_mb:.1f}MB / {total_mb:.1f}MB)",
"downloading_file_unknown_size_text":"'{filename}' をダウンロード中 ({downloaded_mb:.1f}MB)",
"downloading_multipart_text":"DL '{filename}...': {downloaded_mb:.1f}/{total_mb:.1f} MB ({parts}パーツ @ {speed:.2f} MB/s)",
"downloading_multipart_initializing_text":"ファイル: {filename} - パーツを初期化中...",
"status_cancelled_by_user":"ユーザーによってキャンセルされました",
"files_downloaded_label":"ダウンロード済み",
"files_skipped_label":"スキップ済み",
"retry_finished_text":"再試行完了",
"succeeded_text":"成功",
"status_completed":"完了",
"failed_text":"失敗",
"ready_for_new_task_text":"新しいタスクの準備ができました。",
"fav_mode_active_label_text":"⭐ お気に入りモードが有効です。お気に入りのアーティスト/投稿を選択する前に、以下のフィルターを選択してください。下のアクションを選択してください。",
"export_links_button_text":"リンクをエクスポート",
"download_extracted_links_button_text":"ダウンロード",
"log_display_mode_links_view_text":"🔗 リンク表示",
"download_selected_links_dialog_button_text":"選択項目をダウンロード",
"download_external_links_dialog_title":"選択した外部リンクのダウンロード",
"download_external_links_dialog_main_label":"サポートされているリンクが{count}件見つかりました (Mega, GDrive, Dropbox)。ダウンロードするものを選択してください:",
"select_all_button_text":"すべて選択",
"deselect_all_button_text":"すべて選択解除",
"download_selected_button_text":"選択項目をダウンロード",
"link_input_placeholder_text":"例: https://kemono.su/patreon/user/12345 または .../post/98765",
"link_input_tooltip_text":"Kemono/Coomerクリエイターのページまたは特定の投稿の完全なURLを入力します。\n例 (クリエイター): https://kemono.su/patreon/user/12345\n例 (投稿): https://kemono.su/patreon/user/12345/post/98765",
"dir_input_placeholder_text":"ダウンロードを保存するフォルダを選択",
"dir_input_tooltip_text":"ダウンロードされたすべてのコンテンツが保存されるメインフォルダを入力または参照します。\n「リンクのみ」モードが選択されていない限り必須です。",
"character_input_placeholder_text":"例: ティファ, エアリス, (クラウド, ザックス)",
"custom_folder_input_placeholder_text":"任意: この投稿を特定のフォルダに保存",
"custom_folder_input_tooltip_text":"単一の投稿URLをダウンロードし、かつ「名前/タイトルでフォルダを分ける」が有効な場合、\nその投稿のダウンロードフォルダにカスタム名を入力できます。\n例: お気に入りのシーン",
"skip_words_input_placeholder_text":"例: WM, WIP, スケッチ, プレビュー",
"remove_from_filename_input_placeholder_text":"例: patreon, HD",
"cookie_text_input_placeholder_no_file_selected_text":"Cookie文字列 (cookies.txt未選択時)",
"cookie_text_input_placeholder_with_file_selected_text":"選択されたCookieファイルを使用中 (参照...を参照)",
"character_search_input_placeholder_text":"キャラクターを検索...",
"character_search_input_tooltip_text":"既知の番組/キャラクターのリストを以下でフィルタリングするには、ここに入力します。",
"new_char_input_placeholder_text":"新しい番組/キャラクター名を追加",
"new_char_input_tooltip_text":"上記のリストに新しい番組、ゲーム、またはキャラクター名を入力します。",
"link_search_input_placeholder_text":"リンクを検索...",
"link_search_input_tooltip_text":"「リンクのみ」モードの場合、表示されるリンクをテキスト、URL、またはプラットフォームでフィルタリングするには、ここに入力します。",
"manga_date_prefix_input_placeholder_text":"マンガファイル名のプレフィックス",
"manga_date_prefix_input_tooltip_text":"「日付順」または「元ファイル名」マンガファイル名のオプションのプレフィックス（例: 「シリーズ名」）。\n空の場合、ファイルはプレフィックスなしのスタイルに基づいて名前が付けられます。",
"empty_popup_button_tooltip_text":"クリエイター選択を開く\n\n「creators.json」ファイルからクリエイターを閲覧・選択します。\n選択したクリエイター名がURL入力フィールドに追加されます。",
"log_display_mode_progress_view_text":"⬇️ 進捗表示",
"cookie_browse_button_tooltip":"Cookieファイル（Netscape形式、通常はcookies.txt）を参照します。\n「Cookieを使用」がチェックされていて、上のテキストフィールドが空の場合に使用されます。",
"page_range_label_text":"ページ範囲:",
"thread_count_input_tooltip":"同時操作の数。クリエイターフィードの投稿処理または単一投稿のファイルダウンロードに影響します。「マルチスレッドを使用」がオフの場合、1スレッドが使用されます。",
"start_page_input_placeholder":"開始",
"start_page_input_tooltip":"クリエイターURLの場合: ダウンロードを開始する開始ページ番号を指定します（例: 1, 2, 3）。\n最初のページから開始する場合は空白にするか、1に設定します。\n単一投稿URLまたはマンガ/コミックモードでは無効です。",
"page_range_to_label_text":"から",
"end_page_input_placeholder":"終了",
"end_page_input_tooltip":"クリエイターURLの場合: ダウンロードする終了ページ番号を指定します（例: 5, 10）。\n開始ページからすべてのページをダウンロードする場合は空白にします。\n単一投稿URLまたはマンガ/コミックモードでは無効です。",
"known_names_help_button_tooltip_text":"アプリケーション機能ガイドを開きます。",
"future_settings_button_tooltip_text":"アプリケーション設定を開きます（テーマ、言語など）。",
"link_search_button_tooltip_text":"表示されたリンクをフィルター",
"confirm_add_all_dialog_title":"新しい名前の追加を確認",
"confirm_add_all_info_label":"「キャラクターでフィルタリング」入力からの以下の新しい名前/グループは「Known.txt」にありません。\n追加すると、将来のダウンロードのフォルダ整理が改善されます。\n\nリストを確認してアクションを選択してください:",
"confirm_add_all_select_all_button":"すべて選択",
"confirm_add_all_deselect_all_button":"すべて選択解除",
"confirm_add_all_add_selected_button":"選択項目をKnown.txtに追加",
"confirm_add_all_skip_adding_button":"これらの追加をスキップ",
"confirm_add_all_cancel_download_button":"ダウンロードをキャンセル",
"cookie_help_dialog_title":"Cookieファイルの説明",
"cookie_help_instruction_intro":"<p>Cookieを使用するには、通常ブラウザから<b>cookies.txt</b>ファイルが必要です。</p>",
"cookie_help_how_to_get_title":"<p><b>cookies.txtの入手方法:</b></p>",
"cookie_help_step1_extension_intro":"<li>Chromeベースのブラウザに「Get cookies.txt LOCALLY」拡張機能をインストールします:<br><a href=\"https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc\" style=\"color: #87CEEB;\">ChromeウェブストアでGet cookies.txt LOCALLYを入手</a></li>",
"cookie_help_step2_login":"<li>ウェブサイト（例: kemono.suまたはcoomer.su）にアクセスし、必要に応じてログインします。</li>",
"cookie_help_step3_click_icon":"<li>ブラウザのツールバーにある拡張機能のアイコンをクリックします。</li>",
"cookie_help_step4_export":"<li>「エクスポート」ボタン（例: 「名前を付けてエクスポート」、「cookies.txtをエクスポート」 - 正確な文言は拡張機能のバージョンによって異なる場合があります）をクリックします。</li>",
"cookie_help_step5_save_file":"<li>ダウンロードした<code>cookies.txt</code>ファイルをコンピュータに保存します。</li>",
"cookie_help_step6_app_intro":"<li>このアプリケーションで:<ul>",
"cookie_help_step6a_checkbox":"<li>「Cookieを使用」チェックボックスがオンになっていることを確認します。</li>",
"cookie_help_step6b_browse":"<li>Cookieテキストフィールドの隣にある「参照...」ボタンをクリックします。</li>",
"cookie_help_step6c_select":"<li>保存した<code>cookies.txt</code>ファイルを選択します。</li></ul></li>",
"cookie_help_alternative_paste":"<p>または、一部の拡張機能ではCookie文字列を直接コピーできる場合があります。その場合は、ファイルを参照する代わりにテキストフィールドに貼り付けることができます。</p>",
"cookie_help_proceed_without_button":"Cookieなしでダウンロード",
"cookie_help_cancel_download_button":"ダウンロードをキャンセル",
"character_input_tooltip":(
"キャラクター名を入力してください（カンマ区切り）。「フォルダを分ける」が有効な場合、高度なグルーピングに対応し、フォルダ名に影響します。\n\n"
"例:\n"
"- Nami → 'Nami'に一致し、「Nami」フォルダが作成されます。\n"
"- (Ulti, Vivi) → いずれかに一致し、「Ulti Vivi」フォルダが作成され、両方の名前がKnown.txtに個別に追加されます。\n"
"- (Boa, Hancock)~ → いずれかに一致し、「Boa Hancock」フォルダが作成され、Known.txtに1つのグループとして追加されます。\n\n"
"入力された名前は、コンテンツ照合時のエイリアスとして機能します。\n\n"
"フィルターモード（ボタンで切り替え）:\n"
"- ファイル: ファイル名でフィルターします。\n"
"- タイトル: 投稿タイトルでフィルターします。\n"
"- 両方: まず投稿タイトルを確認し、一致しない場合はファイル名を確認します。\n"
"- コメント（ベータ版）: まずファイル名を確認し、一致しない場合は投稿コメントを確認します。"
),
"tour_dialog_title":"Kemonoダウンローダーへようこそ！",
"tour_dialog_never_show_checkbox":"今後このツアーを表示しない",
"tour_dialog_skip_button":"ツアーをスキップ",
"tour_dialog_back_button":"戻る",
"tour_dialog_next_button":"次へ",
"tour_dialog_finish_button":"完了",
"tour_dialog_step1_title":"👋 ようこそ！",
"tour_dialog_step1_content":"""このクイックツアーでは、Kemonoダウンローダーの主な機能（強化されたフィルタリング、マンガモードの改善、Cookie管理など、最近の更新を含む）を説明します。
        <ul>
        <li>私の目標は、<b>Kemono</b>と<b>Coomer</b>からコンテンツを簡単にダウンロードできるようにすることです。</li><br>
        <li><b>🎨 クリエイター選択ボタン:</b> URL入力の隣にあるパレットアイコンをクリックするとダイアログが開きます。<code>creators.json</code>ファイルからクリエイターを閲覧・選択して、URL入力に名前をすばやく追加できます。</li><br>
        <li><b>重要ヒント: アプリが「(応答なし)」になる場合</b><br>
          「ダウンロード開始」をクリックした後、特に大規模なクリエイターフィードや多数のスレッドを使用する場合、アプリケーションが一時的に「(応答なし)」と表示されることがあります。お使いのオペレーティングシステム（Windows、macOS、Linux）が「プロセスの終了」や「強制終了」を提案することさえあるかもしれません。<br>
          <b>しばらくお待ちください！</b> アプリは多くの場合、バックグラウンドで懸命に動作しています。強制終了する前に、選択した「ダウンロード場所」をファイルエクスプローラーで確認してみてください。新しいフォルダが作成されたり、ファイルが表示されたりしている場合は、ダウンロードが正しく進行していることを意味します。応答性が回復するまでしばらく時間をおいてください。</li><br>
        <li><b>次へ</b>と<b>戻る</b>ボタンで移動します。</li><br>
        <li>多くのオプションには、マウスオーバーすると詳細が表示されるツールチップがあります。</li><br>
        <li>いつでもこのガイドを閉じるには<b>ツアーをスキップ</b>をクリックします。</li><br>        
        <li>今後の起動時にこれを見たくない場合は<b>「今後このツアーを表示しない」</b>をチェックします。</li>
        </ul>""",
"tour_dialog_step2_title":"①はじめに",
"tour_dialog_step2_content":"""ダウンロードの基本から始めましょう:
        <ul>
        <li><b>🔗 Kemonoクリエイター/投稿URL:</b><br>
          クリエイターのページ（例: <i>https://kemono.su/patreon/user/12345</i>）
        または特定の投稿（例: <i>.../post/98765</i>）の完全なウェブアドレス（URL）を貼り付けます。</li><br>
          またはCoomerクリエイター（例: <i>https://coomer.su/onlyfans/user/artistname</i>）
        <li><b>📁 ダウンロード場所:</b><br>
          「参照...」をクリックして、ダウンロードしたすべてのファイルが保存されるコンピュータ上のフォルダを選択します。
        「リンクのみ」モードを使用している場合を除き、これは必須です。</li><br>
        <li><b>📄 ページ範囲（クリエイターURLのみ）:</b><br>
          クリエイターのページからダウンロードする場合、取得するページの範囲を指定できます（例: 2ページから5ページ）。
        すべてのページを取得するには空白のままにします。これは単一の投稿URLまたは<b>マンガ/コミックモード</b>がアクティブな場合は無効になります。</li>
        </ul>""",
"tour_dialog_step3_title":"② ダウンロードのフィルタリング",
"tour_dialog_step3_content":"""これらのフィルターでダウンロードするものを絞り込みます（ほとんどは「リンクのみ」または「アーカイブのみ」モードでは無効になります）:
        <ul>
        <li><b>🎯 キャラクターでフィルタリング:</b><br>
          キャラクター名をコンマ区切りで入力します（例: <i>ティファ, エアリス</i>）。結合されたフォルダ名のエイリアスをグループ化します: <i>(エイリアス1, エイリアス2, エイリアス3)</i> は「エイリアス1 エイリアス2 エイリアス3」（クリーニング後）というフォルダになります。グループ内のすべての名前が照合用のエイリアスとして使用されます。<br>
          この入力の隣にある<b>「フィルター: [タイプ]」</b>ボタンは、このフィルターの適用方法を循環します:
          <ul><li><i>フィルター: ファイル:</i> 個々のファイル名を確認します。いずれかのファイルが一致すれば投稿は保持され、一致するファイルのみがダウンロードされます。「フォルダを分ける」がオンの場合、フォルダ名は一致するファイル名のキャラクターを使用します。</li><br>
            <li><i>フィルター: タイトル:</i> 投稿タイトルを確認します。一致する投稿のすべてのファイルがダウンロードされます。フォルダ名は一致する投稿タイトルのキャラクターを使用します。</li>
            <li><b>⤵️ フィルターに追加ボタン（既知の名前）:</b> 既知の名前の「追加」ボタン（ステップ5参照）の隣にあり、これをクリックするとポップアップが開きます。<code>Known.txt</code>リストからチェックボックス（検索バー付き）で名前を選択し、「キャラクターでフィルタリング」フィールドにすばやく追加します。Known.txtの<code>(ボア, ハンコック)</code>のようなグループ化された名前は、フィルターフィールドに<code>(ボア, ハンコック)~</code>として追加されます。</li><br>
            <li><i>フィルター: 両方:</i> まず投稿タイトルを確認します。一致する場合、すべてのファイルがダウンロードされます。一致しない場合、次にファイル名を確認し、一致するファイルのみがダウンロードされます。フォルダ名はタイトル一致を優先し、次にファイル一致を優先します。</li><br>
            <li><i>フィルター: コメント（ベータ）:</i> まずファイル名を確認します。ファイルが一致する場合、投稿のすべてのファイルがダウンロードされます。ファイル一致がない場合、次に投稿コメントを確認します。コメントが一致する場合、投稿のすべてのファイルがダウンロードされます。（より多くのAPIリクエストを使用します）。フォルダ名はファイル一致を優先し、次にコメント一致を優先します。</li></ul>
          「名前/タイトルでフォルダを分ける」が有効な場合、このフィルターはフォルダ名にも影響します。</li><br>
        <li><b>🚫 スキップする単語:</b><br>
          単語をコンマ区切りで入力します（例: <i>WIP, スケッチ, プレビュー</i>）。
          この入力の隣にある<b>「スコープ: [タイプ]」</b>ボタンは、このフィルターの適用方法を循環します:
          <ul><li><i>スコープ: ファイル:</i> 名前にこれらの単語のいずれかを含む場合、ファイルをスキップします。</li><br>
            <li><i>スコープ: 投稿:</i> タイトルにこれらの単語のいずれかを含む場合、投稿全体をスキップします。</li><br>
            <li><i>スコープ: 両方:</i> ファイルと投稿タイトルの両方のスキップを適用します（まず投稿、次にファイル）。</li></ul></li><br>
        <li><b>ファイルフィルター（ラジオボタン）:</b> ダウンロードするものを選択します:
          <ul>
          <li><i>すべて:</i> 見つかったすべてのファイルタイプをダウンロードします。</li><br>
          <li><i>画像/GIF:</i> 一般的な画像形式とGIFのみ。</li><br>
          <li><i>動画:</i> 一般的な動画形式のみ。</li><br>
          <li><b><i>📦 アーカイブのみ:</i></b> <b>.zip</b>と<b>.rar</b>ファイルのみをダウンロードします。選択すると、「.zipをスキップ」と「.rarをスキップ」チェックボックスは自動的に無効になり、チェックが外れます。「外部リンクをログに表示」も無効になります。</li><br>
          <li><i>🎧 音声のみ:</i> 一般的な音声形式のみ（MP3、WAV、FLACなど）。</li><br>
          <li><i>🔗 リンクのみ:</i> ファイルをダウンロードする代わりに、投稿の説明から外部リンクを抽出して表示します。ダウンロード関連のオプションと「外部リンクをログに表示」は無効になります。</li>
          </ul></li>
        </ul>""",
"tour_dialog_step4_title":"③ お気に入りモード（代替ダウンロード）",
"tour_dialog_step4_content":"""アプリケーションは、Kemono.suでお気に入りに登録したアーティストからコンテンツをダウンロードするための「お気に入りモード」を提供しています。
        <ul>
        <li><b>⭐ お気に入りモードチェックボックス:</b><br>
          「🔗 リンクのみ」ラジオボタンの隣にあります。これをチェックするとお気に入りモードが有効になります。</li><br>
        <li><b>お気に入りモードでの動作:</b>
          <ul><li>「🔗 Kemonoクリエイター/投稿URL」入力エリアは、お気に入りモードがアクティブであることを示すメッセージに置き換えられます。</li><br>
            <li>標準の「ダウンロード開始」、「一時停止」、「キャンセル」ボタンは、「🖼️ お気に入りアーティスト」と「📄 お気に入り投稿」ボタンに置き換えられます（注意: 「お気に入り投稿」は将来の機能です）。</li><br>
            <li>お気に入りを取得するにはCookieが必要なため、「🍪 Cookieを使用」オプションは自動的に有効になり、ロックされます。</li></ul></li><br>
        <li><b>🖼️ お気に入りアーティストボタン:</b><br>
          これをクリックすると、Kemono.suでお気に入りに登録したアーティストのリストが表示されるダイアログが開きます。このリストから1人以上のアーティストを選択してダウンロードできます。</li><br>
        <li><b>お気に入りダウンロードスコープ（ボタン）:</b><br>
          このボタン（「お気に入り投稿」の隣）は、選択したお気に入りのダウンロード場所を制御します:
          <ul><li><i>スコープ: 選択場所:</i> 選択したすべてのアーティストは、UIで設定したメインの「ダウンロード場所」にダウンロードされます。フィルターはグローバルに適用されます。</li><br>
            <li><i>スコープ: アーティストフォルダ:</i> 選択した各アーティストについて、メインの「ダウンロード場所」内にサブフォルダ（アーティスト名）が作成されます。そのアーティストのコンテンツは、特定のサブフォルダにダウンロードされます。フィルターは各アーティストのフォルダ内で適用されます。</li></ul></li><br>
        <li><b>お気に入りモードでのフィルター:</b><br>
          「キャラクターでフィルタリング」、「スキップする単語」、「ファイルフィルター」オプションは、選択したお気に入りアーティストからダウンロードされるコンテンツにも適用されます。</li>
        </ul>""",
"tour_dialog_step5_title":"④ ダウンロードの微調整",
"tour_dialog_step5_content":"""ダウンロードをカスタマイズするためのその他のオプション:
        <ul>
        <li><b>.zipをスキップ / .rarをスキップ:</b> これらのアーカイブファイルタイプをダウンロードしないようにするには、これらをチェックします。
          <i>（注意: 「📦 アーカイブのみ」フィルターモードが選択されている場合、これらは無効になり、無視されます）。</i></li><br>
        <li><b>✂️ 名前から単語を削除:</b><br>
          ダウンロードしたファイル名から削除する単語をコンマ区切りで入力します（大文字と小文字を区別しません）（例: <i>patreon, [HD]</i>）。</li><br>
        <li><b>サムネイルのみダウンロード:</b> フルサイズのファイルの代わりに小さなプレビュー画像をダウンロードします（利用可能な場合）。</li><br>
        <li><b>大きな画像を圧縮:</b> 「Pillow」ライブラリがインストールされている場合、1.5MBより大きい画像は、WebPバージョンが大幅に小さい場合にWebP形式に変換されます。</li><br>
        <li><b>🗄️ カスタムフォルダ名（単一投稿のみ）:</b><br>
          単一の特定の投稿URLをダウンロードしていて、かつ「名前/タイトルでフォルダを分ける」が有効な場合、
        その投稿のダウンロードフォルダにカスタム名を入力できます。</li><br>
        <li><b>🍪 Cookieを使用:</b> リクエストにCookieを使用するには、これをチェックします。次のいずれかを実行できます:
          <ul><li>Cookie文字列をテキストフィールドに直接入力します（例: <i>name1=value1; name2=value2</i>）。</li><br>
            <li>「参照...」をクリックして<i>cookies.txt</i>ファイル（Netscape形式）を選択します。パスがテキストフィールドに表示されます。</li></ul>
          これは、ログインが必要なコンテンツにアクセスする場合に便利です。テキストフィールド（入力されている場合）が優先されます。
        「Cookieを使用」がチェックされていて、テキストフィールドと参照されたファイルの両方が空の場合、アプリのディレクトリから「cookies.txt」を読み込もうとします。</li>
        </ul>""",
"tour_dialog_step6_title":"⑤ 整理とパフォーマンス",
"tour_dialog_step6_content":"""ダウンロードを整理し、パフォーマンスを管理します:
        <ul>
        <li><b>⚙️ 名前/タイトルでフォルダを分ける:</b> 「キャラクターでフィルタリング」入力または投稿タイトルに基づいてサブフォルダを作成します（特定のフィルターが投稿に一致しない場合、フォルダ名のフォールバックとして<b>Known.txt</b>リストを使用できます）。</li><br>
        <li><b>投稿ごとにサブフォルダ:</b> 「フォルダを分ける」がオンの場合、メインのキャラクター/タイトルフォルダ内に<i>個々の投稿</i>ごとに追加のサブフォルダを作成します。</li><br>
        <li><b>🚀 マルチスレッドを使用（スレッド数）:</b> より高速な操作を可能にします。「スレッド数」入力の数値の意味:
          <ul><li><b>クリエイターフィードの場合:</b> 同時に処理する投稿の数。各投稿内のファイルは、そのワーカーによって順番にダウンロードされます（「日付順」マンガ命名がオンの場合を除く。これは1つの投稿ワーカーを強制します）。</li><br>
            <li><b>単一投稿URLの場合:</b> その単一投稿から同時にダウンロードするファイルの数。</li></ul>
          チェックされていない場合、1スレッドが使用されます。高いスレッド数（例: >40）はアドバイザリを表示する場合があります。</li><br>
        <li><b>マルチパートダウンロード切り替え（ログエリアの右上）:</b><br>
          <b>「マルチパート: [オン/オフ]」</b>ボタンは、個々の大きなファイルのマルチセグメントダウンロードを有効/無効にできます。
          <ul><li><b>オン:</b> 大きなファイルのダウンロード（例: 動画）を高速化できますが、多くの小さなファイルがある場合、UIの途切れやログのスパムが増加する可能性があります。有効にするとアドバイザリが表示されます。マルチパートダウンロードが失敗した場合、シングルストリームで再試行します。</li><br>
            <li><b>オフ（デフォルト）:</b> ファイルは単一のストリームでダウンロードされます。</li></ul>
          「リンクのみ」または「アーカイブのみ」モードがアクティブな場合は無効になります。</li><br>
        <li><b>📖 マンガ/コミックモード（クリエイターURLのみ）:</b> シーケンシャルコンテンツ向けに調整されています。
          <ul>
          <li>投稿を<b>古いものから新しいものへ</b>ダウンロードします。</li><br>
          <li>すべての投稿が取得されるため、「ページ範囲」入力は無効になります。</li><br>
          <li>このモードがクリエイターフィードでアクティブな場合、ログエリアの右上に<b>ファイル名スタイル切り替えボタン</b>（例: 「名前: 投稿タイトル」）が表示されます。クリックすると命名スタイルが循環します:
            <ul>
            <li><b><i>名前: 投稿タイトル（デフォルト）:</i></b> 投稿の最初のファイルは、投稿のクリーンなタイトルにちなんで名付けられます（例: 「My Chapter 1.jpg」）。*同じ投稿*内の後続のファイルは、元のファイル名を保持しようとします（例: 「page_02.png」、「bonus_art.jpg」）。投稿にファイルが1つしかない場合は、投稿タイトルにちなんで名付けられます。これはほとんどのマンガ/コミックに一般的に推奨されます。</li><br>
            <li><b><i>名前: 元ファイル名:</i></b> すべてのファイルが元のファイル名を保持しようとします。オプションのプレフィックス（例: 「MySeries_」）を、このスタイルボタンの隣に表示される入力フィールドに入力できます。例: 「MySeries_OriginalFile.jpg」。</li><br>
            <li><b><i>名前: タイトル+通し番号（投稿タイトル+グローバル番号付け）:</i></b> 現在のダウンロードセッションのすべての投稿のすべてのファイルが、投稿のクリーンなタイトルをプレフィックスとして使用し、グローバルカウンターを続けて順番に名付けられます。例: 投稿「Chapter 1」（2ファイル）-> 「Chapter 1_001.jpg」、「Chapter 1_002.png」。次の投稿「Chapter 2」（1ファイル）は番号付けを続けます -> 「Chapter 2_003.jpg」。このスタイルの場合、正しいグローバル番号付けを保証するために、投稿処理のマルチスレッドは自動的に無効になります。</li><br>
            <li><b><i>名前: 日付順:</i></b> ファイルは投稿の公開順に基づいて順番に名付けられます（001.ext、002.extなど）。オプションのプレフィックス（例: 「MySeries_」）を、このスタイルボタンの隣に表示される入力フィールドに入力できます。例: 「MySeries_001.jpg」。このスタイルの場合、投稿処理のマルチスレッドは自動的に無効になります。</li>
            </ul>
          </li><br>
          <li>「名前: 投稿タイトル」、「名前: タイトル+通し番号」、または「名前: 日付順」スタイルで最良の結果を得るには、「キャラクターでフィルタリング」フィールドにマンガ/シリーズのタイトルを入力してフォルダを整理します。</li>
          </ul></li><br>
        <li><b>🎭 Known.txtによるスマートなフォルダ整理:</b><br>
          <code>Known.txt</code>（アプリのディレクトリ内）は、「名前/タイトルでフォルダを分ける」がアクティブな場合の自動フォルダ整理を細かく制御できます。
          <ul> # JA_PLACEHOLDER
            <li><b>仕組み:</b> <code>Known.txt</code>の各行がエントリです。
              <ul><li><code>My Awesome Series</code>のような単純な行は、これに一致するコンテンツが「My Awesome Series」という名前のフォルダに入ることを意味します。</li><br>
                <li><code>(Character A, Char A, Alt Name A)</code>のようなグループ化された行は、「Character A」、「Char A」、または「Alt Name A」に一致するコンテンツがすべて「Character A Char A Alt Name A」（クリーニング後）という名前の単一フォルダに入ることを意味します。括弧内のすべての用語がそのフォルダのエイリアスになります。</li></ul></li>
            <li><b>インテリジェントなフォールバック:</b> 「名前/タイトルでフォルダを分ける」がアクティブで、投稿が特定の「キャラクターでフィルタリング」入力に一致しない場合、ダウンローダーは<code>Known.txt</code>を参照して、フォルダ作成用の一致するプライマリ名を見つけます。</li><br>
            <li><b>ユーザーフレンドリーな管理:</b> UIリスト（下記）から単純な（グループ化されていない）名前を追加します。高度な編集（グループ化されたエイリアスの作成/変更など）の場合は、<b>「Known.txtを開く」</b>をクリックしてテキストエディタでファイルを編集します。アプリは次回使用時または起動時に再読み込みします。</li>
          </ul>
        </li>
        </ul>""",
"tour_dialog_step7_title":"⑥ 一般的なエラーとトラブルシューティング",
"tour_dialog_step7_content":"""ダウンロード中に問題が発生することがあります。一般的なものをいくつか紹介します:
        <ul>
        <li><b>キャラクター入力ツールチップ:</b><br>
          キャラクター名をコンマ区切りで入力します (例: <i>ティファ, エアリス</i>)。<br>
          結合されたフォルダ名のエイリアスをグループ化します: <i>(エイリアス1, エイリアス2, エイリアス3)</i> はフォルダ「エイリアス1 エイリアス2 エイリアス3」になります。<br>
          グループ内のすべての名前が照合用のエイリアスとして使用されます。<br><br>
          この入力の隣にある「フィルター: [タイプ]」ボタンは、このフィルターの適用方法を循環します:<br>
          - フィルター: ファイル: 個々のファイル名を確認します。一致するファイルのみがダウンロードされます。<br>
          - フィルター: タイトル: 投稿タイトルを確認します。一致する投稿のすべてのファイルがダウンロードされます。<br>
          - フィルター: 両方: まず投稿タイトルを確認します。一致しない場合、次にファイル名を確認します。<br>
          - フィルター: コメント (ベータ): まずファイル名を確認します。一致しない場合、次に投稿コメントを確認します。<br><br>
          「名前/タイトルでフォルダを分ける」が有効な場合、このフィルターはフォルダ名にも影響します。</li><br>      
        <li><b>502 Bad Gateway / 503 Service Unavailable / 504 Gateway Timeout:</b><br>
          これらは通常、Kemono/Coomerのサーバー側の一時的な問題を示します。サイトが過負荷になっているか、メンテナンス中であるか、問題が発生している可能性があります。<br>
          <b>解決策:</b> しばらく（例: 30分から数時間）待ってから、後でもう一度試してください。ブラウザで直接サイトを確認してください。</li><br>
        <li><b>接続喪失 / 接続拒否 / タイムアウト（ファイルダウンロード中）:</b><br>
          これは、インターネット接続、サーバーの不安定性、またはサーバーが大きなファイルの接続を切断した場合に発生する可能性があります。<br>
          <b>解決策:</b> インターネットを確認してください。「スレッド数」が高い場合は減らしてみてください。セッションの最後に一部の失敗したファイルを再試行するようアプリが促す場合があります。</li><br>
        <li><b>IncompleteReadエラー:</b><br>
          サーバーが予期したよりも少ないデータを送信しました。多くの場合、一時的なネットワークの不具合またはサーバーの問題です。<br>
          <b>解決策:</b> アプリは多くの場合、ダウンロードセッションの最後にこれらのファイルを再試行対象としてマークします。</li><br>
        <li><b>403 Forbidden / 401 Unauthorized（公開投稿ではあまり一般的ではありません）:</b><br>
          コンテンツにアクセスする権限がない可能性があります。一部の有料またはプライベートコンテンツの場合、「Cookieを使用」オプションをブラウザセッションの有効なCookieと共に使用すると役立つ場合があります。Cookieが最新であることを確認してください。</li><br>
        <li><b>404 Not Found:</b><br>
          投稿またはファイルのURLが正しくないか、コンテンツがサイトから削除されています。URLを再確認してください。</li><br>
        <li><b>「投稿が見つかりません」/「対象の投稿が見つかりません」:</b><br>
          URLが正しく、クリエイター/投稿が存在することを確認してください。ページ範囲を使用している場合は、クリエイターに対して有効であることを確認してください。非常に新しい投稿の場合、APIに表示されるまでにわずかな遅延がある場合があります。</li><br>
        <li><b>全体的な遅さ / アプリ「(応答なし)」:</b><br>
          ステップ1で述べたように、特に大規模なクリエイターフィードや多くのスレッドで開始後にアプリがハングするように見える場合は、しばらくお待ちください。バックグラウンドでデータを処理している可能性が高いです。これが頻繁に発生する場合は、スレッド数を減らすと応答性が向上することがあります。</li>
        </ul>""",
"tour_dialog_step8_title":"⑦ ログと最終コントロール",
"tour_dialog_step8_content":"""監視とコントロール:
        <ul>
        <li><b>📜 進捗ログ / 抽出リンクログ:</b> 詳細なダウンロードメッセージを表示します。「🔗 リンクのみ」モードがアクティブな場合、このエリアには抽出されたリンクが表示されます。</li><br>
        <li><b>ログに外部リンクを表示:</b> チェックすると、メインログの下にセカンダリログパネルが表示され、投稿の説明で見つかった外部リンクが表示されます。<i>（「🔗 リンクのみ」または「📦 アーカイブのみ」モードがアクティブな場合は無効になります）。</i></li><br>
        <li><b>ログビュー切り替え（👁️ / 🙈 ボタン）:</b><br>
          このボタン（ログエリアの右上）は、メインログビューを切り替えます:
          <ul><li><b>👁️ 進捗ログ（デフォルト）:</b> すべてのダウンロードアクティビティ、エラー、概要を表示します。</li><br>
            <li><b>🙈 見逃したキャラクターログ:</b> 「キャラクターでフィルタリング」設定のためにスキップされた投稿タイトルのキーワードのリストを表示します。意図せずに見逃している可能性のあるコンテンツを特定するのに役立ちます。</li></ul></li><br>
        <li><b>🔄 リセット:</b> すべての入力フィールド、ログをクリアし、一時的な設定をデフォルトにリセットします。ダウンロードがアクティブでない場合にのみ使用できます。</li><br>
        <li><b>⬇️ ダウンロード開始 / 🔗 リンクを抽出 / ⏸️ 一時停止 / ❌ 中止:</b> これらのボタンでプロセスを制御します。「中止してUIリセット」は現在の操作を停止し、URLとディレクトリ入力を保持してソフトUIリセットを実行します。「一時停止/再開」は一時的な停止と継続を可能にします。</li><br>
        <li>一部のファイルが回復可能なエラー（「IncompleteRead」など）で失敗した場合、セッションの最後に再試行するよう促される場合があります。</li>
        </ul>
        <br>準備完了です！<b>「完了」</b>をクリックしてツアーを閉じ、ダウンローダーの使用を開始します。"""
}
}

translations ["fr"]={
"settings_dialog_title":"Paramètres",
"language_label":"Langue :",
"lang_english":"Anglais (English)",
"lang_japanese":"Japonais (日本語)",
"theme_toggle_light":"Passer en mode clair",
"theme_toggle_dark":"Passer en mode sombre",
"theme_tooltip_light":"Changer l'apparence de l'application en clair.",
"theme_tooltip_dark":"Changer l'apparence de l'application en sombre.",
"ok_button":"OK",
"appearance_group_title":"Apparence",
"language_group_title":"Paramètres de langue",
"creator_post_url_label":"🔗 URL Créateur/Post Kemono :",
"download_location_label":"📁 Emplacement de téléchargement :",
"filter_by_character_label":"🎯 Filtrer par Personnage(s) (séparés par des virgules) :",
"skip_with_words_label":"🚫 Ignorer avec les mots (séparés par des virgules) :",
"remove_words_from_name_label":"✂️ Supprimer les mots du nom :",
"filter_all_radio":"Tout",
"filter_images_radio":"Images/GIFs",
"filter_videos_radio":"Vidéos",
"filter_archives_radio":"📦 Archives Uniquement",
"filter_links_radio":"🔗 Liens Uniquement",
"filter_audio_radio":"🎧 Audio Uniquement",
"favorite_mode_checkbox_label":"⭐ Mode Favori",
"browse_button_text":"Parcourir...",
"char_filter_scope_files_text":"Filtre : Fichiers",
"char_filter_scope_files_tooltip":"Portée actuelle : Fichiers\n\nFiltre les fichiers individuels par nom. Une publication est conservée si un fichier correspond.\nSeuls les fichiers correspondants de cette publication sont téléchargés.\nExemple : Filtre 'Tifa'. Le fichier 'Tifa_artwork.jpg' correspond et est téléchargé.\nNommage du dossier : Utilise le personnage du nom de fichier correspondant.\n\nCliquez pour passer à : Les deux",
"char_filter_scope_title_text":"Filtre : Titre",
"char_filter_scope_title_tooltip":"Portée actuelle : Titre\n\nFiltre les publications entières par leur titre. Tous les fichiers d'une publication correspondante sont téléchargés.\nExemple : Filtre 'Aerith'. La publication intitulée 'Le jardin d'Aerith' correspond ; tous ses fichiers sont téléchargés.\nNommage du dossier : Utilise le personnage du titre de la publication correspondante.\n\nCliquez pour passer à : Fichiers",
"char_filter_scope_both_text":"Filtre : Les deux",
"char_filter_scope_both_tooltip":"Portée actuelle : Les deux (Titre puis Fichiers)\n\n1. Vérifie le titre de la publication : S'il correspond, tous les fichiers de la publication sont téléchargés.\n2. Si le titre ne correspond pas, vérifie les noms de fichiers : Si un fichier correspond, seul ce fichier est téléchargé.\nExemple : Filtre 'Cloud'.\n - Publication 'Cloud Strife' (correspondance de titre) -> tous les fichiers sont téléchargés.\n - Publication 'Course de moto' avec 'Cloud_fenrir.jpg' (correspondance de fichier) -> seul 'Cloud_fenrir.jpg' est téléchargé.\nNommage du dossier : Priorise la correspondance de titre, puis la correspondance de fichier.\n\nCliquez pour passer à : Commentaires",
"char_filter_scope_comments_text":"Filtre : Commentaires (Bêta)",
"char_filter_scope_comments_tooltip":"Portée actuelle : Commentaires (Bêta - Fichiers d'abord, puis Commentaires en repli)\n\n1. Vérifie les noms de fichiers : Si un fichier dans la publication correspond au filtre, la publication entière est téléchargée. Les commentaires ne sont PAS vérifiés pour ce terme de filtre.\n2. Si aucun fichier ne correspond, ALORS vérifie les commentaires de la publication : Si un commentaire correspond, la publication entière est téléchargée.\nExemple : Filtre 'Barret'.\n - Publication A : Fichiers 'Barret_gunarm.jpg', 'other.png'. Le fichier 'Barret_gunarm.jpg' correspond. Tous les fichiers de la publication A sont téléchargés. Les commentaires ne sont pas vérifiés pour 'Barret'.\n - Publication B : Fichiers 'dyne.jpg', 'weapon.gif'. Commentaires : '...un dessin de Barret Wallace...'. Aucune correspondance de fichier pour 'Barret'. Le commentaire correspond. Tous les fichiers de la publication B sont téléchargés.\nNommage du dossier : Priorise le personnage de la correspondance de fichier, puis de la correspondance de commentaire.\n\nCliquez pour passer à : Titre",
"char_filter_scope_unknown_text":"Filtre : Inconnu",
"char_filter_scope_unknown_tooltip":"Portée actuelle : Inconnue\n\nLa portée du filtre de personnage est dans un état inconnu. Veuillez cycler ou réinitialiser.\n\nCliquez pour passer à : Titre",
"skip_words_input_tooltip":"Saisissez des mots, séparés par des virgules, pour ignorer le téléchargement de certains contenus (par ex., WIP, sketch, preview).\n\nLe bouton 'Portée : [Type]' à côté de cette entrée change la façon dont ce filtre s'applique :\n- Portée : Fichiers : Ignore les fichiers individuels si leurs noms contiennent l'un de ces mots.\n- Portée : Publications : Ignore les publications entières si leurs titres contiennent l'un de ces mots.\n- Portée : Les deux : Applique les deux (titre de la publication d'abord, puis fichiers individuels si le titre de la publication est OK).",
"remove_words_input_tooltip":"Saisissez des mots, séparés par des virgules, à supprimer des noms de fichiers téléchargés (insensible à la casse).\nUtile pour nettoyer les préfixes/suffixes courants.\nExemple : patreon, kemono, [HD], _final",
"skip_scope_files_text":"Portée : Fichiers",
"skip_scope_files_tooltip":"Portée d'omission actuelle : Fichiers\n\nIgnore les fichiers individuels si leurs noms contiennent l'un des 'Mots à ignorer'.\nExemple : Mots à ignorer \"WIP, sketch\".\n- Fichier \"art_WIP.jpg\" -> IGNORÉ.\n- Fichier \"final_art.png\" -> TÉLÉCHARGÉ (si les autres conditions sont remplies).\n\nLa publication est toujours traitée pour les autres fichiers non ignorés.\nCliquez pour passer à : Les deux",
"skip_scope_posts_text":"Portée : Publications",
"skip_scope_posts_tooltip":"Portée d'omission actuelle : Publications\n\nIgnore les publications entières si leurs titres contiennent l'un des 'Mots à ignorer'.\nTous les fichiers d'une publication ignorée sont ignorés.\nExemple : Mots à ignorer \"preview, announcement\".\n- Publication \"Annonce excitante !\" -> IGNORÉE.\n- Publication \"Œuvre terminée\" -> TRAITÉE (si les autres conditions sont remplies).\n\nCliquez pour passer à : Fichiers",
"skip_scope_both_text":"Portée : Les deux",
"skip_scope_both_tooltip":"Portée d'omission actuelle : Les deux (Publications puis Fichiers)\n\n1. Vérifie le titre de la publication : Si le titre contient un mot à ignorer, la publication entière est IGNORÉE.\n2. Si le titre de la publication est OK, alors vérifie les noms de fichiers individuels : Si un nom de fichier contient un mot à ignorer, seul ce fichier est IGNORÉ.\nExemple : Mots à ignorer \"WIP, sketch\".\n- Publication \"Croquis et WIPs\" (correspondance de titre) -> PUBLICATION ENTIÈRE IGNORÉE.\n- Publication \"Mise à jour artistique\" (titre OK) avec les fichiers :\n  - \"character_WIP.jpg\" (correspondance de fichier) -> IGNORÉ.\n  - \"final_scene.png\" (fichier OK) -> TÉLÉCHARGÉ.\n\nCliquez pour passer à : Publications",
"skip_scope_unknown_text":"Portée : Inconnue",
"skip_scope_unknown_tooltip":"Portée d'omission actuelle : Inconnue\n\nLa portée des mots à ignorer est dans un état inconnu. Veuillez cycler ou réinitialiser.\n\nCliquez pour passer à : Publications",
"language_change_title":"Langue modifiée",
"language_change_message":"La langue a été modifiée. Un redémarrage est nécessaire pour que toutes les modifications prennent pleinement effet.",
"language_change_informative":"Voulez-vous redémarrer l'application maintenant ?",
"restart_now_button":"Redémarrer maintenant",
"skip_zip_checkbox_label":"Ignorer .zip",
"skip_rar_checkbox_label":"Ignorer .rar",
"download_thumbnails_checkbox_label":"Télécharger les miniatures uniquement",
"scan_content_images_checkbox_label":"Analyser le contenu pour les images",
"compress_images_checkbox_label":"Compresser en WebP",
"separate_folders_checkbox_label":"Dossiers séparés par Nom/Titre",
"subfolder_per_post_checkbox_label":"Sous-dossier par publication",
"use_cookie_checkbox_label":"Utiliser le cookie",
"use_multithreading_checkbox_base_label":"Utiliser le multithreading",
"show_external_links_checkbox_label":"Afficher les liens externes dans le journal",
"manga_comic_mode_checkbox_label":"Mode Manga/BD",
"threads_label":"Threads :",
"start_download_button_text":"⬇️ Démarrer le téléchargement",
"start_download_button_tooltip":"Cliquez pour démarrer le processus de téléchargement ou d'extraction de liens avec les paramètres actuels.",
"extract_links_button_text":"🔗 Extraire les liens",
"pause_download_button_text":"⏸️ Mettre en pause le téléchargement",
"pause_download_button_tooltip":"Cliquez pour mettre en pause le processus de téléchargement en cours.",
"resume_download_button_text":"▶️ Reprendre le téléchargement",
"resume_download_button_tooltip":"Cliquez pour reprendre le téléchargement.",
"cancel_button_text":"❌ Annuler & Réinitialiser l'UI",
"cancel_button_tooltip":"Cliquez pour annuler le processus de téléchargement/extraction en cours et réinitialiser les champs de l'UI (en conservant l'URL et le répertoire).",
"error_button_text":"Erreur",
"error_button_tooltip":"Voir les fichiers ignorés en raison d'erreurs et éventuellement les réessayer.",
"cancel_retry_button_text":"❌ Annuler la nouvelle tentative",
"known_chars_label_text":"🎭 Séries/Personnages connus (pour les noms de dossiers) :",
"open_known_txt_button_text":"Ouvrir Known.txt",
"known_chars_list_tooltip":"Cette liste contient les noms utilisés pour la création automatique de dossiers lorsque 'Dossiers séparés' est activé\net qu'aucun 'Filtrer par Personnage(s)' spécifique n'est fourni ou ne correspond à une publication.\nAjoutez les noms des séries, jeux ou personnages que vous téléchargez fréquemment.",
"open_known_txt_button_tooltip":"Ouvrir le fichier 'Known.txt' dans votre éditeur de texte par défaut.\nLe fichier se trouve dans le répertoire de l'application.",
"add_char_button_text":"➕ Ajouter",
"add_char_button_tooltip":"Ajouter le nom du champ de saisie à la liste 'Séries/Personnages connus'.",
"add_to_filter_button_text":"⤵️ Ajouter au filtre",
"add_to_filter_button_tooltip":"Sélectionnez des noms dans la liste 'Séries/Personnages connus' pour les ajouter au champ 'Filtrer par Personnage(s)' ci-dessus.",
"delete_char_button_text":"🗑️ Supprimer la sélection",
"delete_char_button_tooltip":"Supprimer le(s) nom(s) sélectionné(s) de la liste 'Séries/Personnages connus'.",
"progress_log_label_text":"📜 Journal de progression :",
"radio_all_tooltip":"Télécharger tous les types de fichiers trouvés dans les publications.",
"radio_images_tooltip":"Télécharger uniquement les formats d'image courants (JPG, PNG, GIF, WEBP, etc.).",
"radio_videos_tooltip":"Télécharger uniquement les formats vidéo courants (MP4, MKV, WEBM, MOV, etc.).",
"radio_only_archives_tooltip":"Télécharger exclusivement les fichiers .zip et .rar. Les autres options spécifiques aux fichiers sont désactivées.",
"radio_only_audio_tooltip":"Télécharger uniquement les formats audio courants (MP3, WAV, FLAC, etc.).",
"radio_only_links_tooltip":"Extraire et afficher les liens externes des descriptions de publications au lieu de télécharger des fichiers.\nLes options liées au téléchargement seront désactivées.",
"favorite_mode_checkbox_tooltip":"Activer le Mode Favori pour parcourir les artistes/publications enregistrés.\nCela remplacera le champ de saisie de l'URL par des boutons de sélection de Favoris.",
"skip_zip_checkbox_tooltip":"Si coché, les fichiers d'archive .zip ne seront pas téléchargés.\n(Désactivé si 'Archives Uniquement' est sélectionné).",
"skip_rar_checkbox_tooltip":"Si coché, les fichiers d'archive .rar ne seront pas téléchargés.\n(Désactivé si 'Archives Uniquement' est sélectionné).",
"download_thumbnails_checkbox_tooltip":"Télécharge les petites images d'aperçu de l'API au lieu des fichiers en taille réelle (si disponible).\nSi 'Analyser le contenu de la publication pour les URL d'images' est également coché, ce mode ne téléchargera *que* les images trouvées par l'analyse de contenu (ignorant les miniatures de l'API).",
"scan_content_images_checkbox_tooltip":"Si coché, le téléchargeur analysera le contenu HTML des publications à la recherche d'URL d'images (à partir des balises <img> ou des liens directs).\nCela inclut la résolution des chemins relatifs des balises <img> en URL complètes.\nLes chemins relatifs dans les balises <img> (par ex., /data/image.jpg) seront résolus en URL complètes.\nUtile pour les cas où les images se trouvent dans la description de la publication mais pas dans la liste des fichiers/pièces jointes de l'API.",
"compress_images_checkbox_tooltip":"Compresser les images > 1.5 Mo au format WebP (nécessite Pillow).",
"use_subfolders_checkbox_tooltip":"Créer des sous-dossiers basés sur l'entrée 'Filtrer par Personnage(s)' ou les titres des publications.\nUtilise la liste 'Séries/Personnages connus' comme solution de repli pour les noms de dossiers si aucun filtre spécifique ne correspond.\nActive l'entrée 'Filtrer par Personnage(s)' et 'Nom de dossier personnalisé' pour les publications uniques.",
"use_subfolder_per_post_checkbox_tooltip":"Crée un sous-dossier pour chaque publication. Si 'Dossiers séparés' est également activé, il se trouve à l'intérieur du dossier personnage/titre.",
"use_cookie_checkbox_tooltip":"Si coché, tentera d'utiliser les cookies de 'cookies.txt' (format Netscape)\ndans le répertoire de l'application pour les requêtes.\nUtile pour accéder au contenu nécessitant une connexion sur Kemono/Coomer.",
"cookie_text_input_tooltip":"Saisissez votre chaîne de cookie directement.\nCelle-ci sera utilisée si 'Utiliser le cookie' est coché ET si 'cookies.txt' n'est pas trouvé ou si ce champ n'est pas vide.\nLe format dépend de la manière dont le backend l'analysera (par ex., 'nom1=valeur1; nom2=valeur2').",
"use_multithreading_checkbox_tooltip":"Active les opérations concurrentes. Voir le champ 'Threads' pour plus de détails.",
"thread_count_input_tooltip":"Nombre d'opérations concurrentes.\n- Publication unique : Téléchargements de fichiers concurrents (1-10 recommandé).\n- URL de flux de créateur : Nombre de publications à traiter simultanément (1-200 recommandé).\n  Les fichiers de chaque publication sont téléchargés un par un par son worker.\nSi 'Utiliser le multithreading' est décoché, 1 thread est utilisé.",
"external_links_checkbox_tooltip":"Si coché, un panneau de journal secondaire apparaît sous le journal principal pour afficher les liens externes trouvés dans les descriptions de publications.\n(Désactivé si le mode 'Liens Uniquement' ou 'Archives Uniquement' est actif).",
"manga_mode_checkbox_tooltip":"Télécharge les publications du plus ancien au plus récent et renomme les fichiers en fonction du titre de la publication (pour les flux de créateurs uniquement).",
"multipart_on_button_text":"Multi-partie : ON",
"multipart_on_button_tooltip":"Téléchargement multi-partie : ON\n\nActive le téléchargement de gros fichiers en plusieurs segments simultanément.\n- Peut accélérer les téléchargements de fichiers volumineux uniques (par ex., des vidéos).\n- Peut augmenter l'utilisation du CPU/réseau.\n- Pour les flux avec de nombreux petits fichiers, cela pourrait ne pas offrir d'avantages en termes de vitesse et pourrait rendre l'UI/le journal chargé.\n- Si le multi-partie échoue, il réessaie en flux unique.\n\nCliquez pour désactiver.",
"multipart_off_button_text":"Multi-partie : OFF",
"multipart_off_button_tooltip":"Téléchargement multi-partie : OFF\n\nTous les fichiers sont téléchargés en utilisant un seul flux.\n- Stable et fonctionne bien pour la plupart des scénarios, en particulier de nombreux petits fichiers.\n- Gros fichiers téléchargés séquentiellement.\n\nCliquez pour activer (voir l'avertissement).",
"reset_button_text":"🔄 Réinitialiser",
"reset_button_tooltip":"Réinitialiser toutes les entrées et les journaux à leur état par défaut (uniquement lorsque l'application est inactive).",
"progress_idle_text":"Progression : Inactif",
"missed_character_log_label_text":"🚫 Journal des personnages manqués :",
"creator_popup_title":"Sélection du créateur",
"creator_popup_search_placeholder":"Rechercher par nom, service, ou coller l'URL du créateur...",
"creator_popup_add_selected_button":"Ajouter la sélection",
"creator_popup_scope_characters_button":"Portée : Personnages",
"creator_popup_scope_creators_button":"Portée : Créateurs",
"favorite_artists_button_text":"🖼️ Artistes favoris",
"favorite_artists_button_tooltip":"Parcourez et téléchargez depuis vos artistes favoris sur Kemono.su/Coomer.su.",
"favorite_posts_button_text":"📄 Publications favorites",
"favorite_posts_button_tooltip":"Parcourez et téléchargez vos publications favorites depuis Kemono.su/Coomer.su.",
"favorite_scope_selected_location_text":"Portée : Emplacement sélectionné",
"favorite_scope_selected_location_tooltip":"Portée de téléchargement des favoris actuelle : Emplacement sélectionné\n\nTous les artistes/publications favoris sélectionnés seront téléchargés dans l' 'Emplacement de téléchargement' principal spécifié dans l'UI.\nLes filtres (personnage, mots à ignorer, type de fichier) s'appliqueront globalement à tout le contenu.\n\nCliquez pour changer pour : Dossiers d'artistes",
"favorite_scope_artist_folders_text":"Portée : Dossiers d'artistes",
"favorite_scope_artist_folders_tooltip":"Portée de téléchargement des favoris actuelle : Dossiers d'artistes\n\nPour chaque artiste/publication favori sélectionné, un nouveau sous-dossier (nommé d'après l'artiste) sera créé à l'intérieur de l' 'Emplacement de téléchargement' principal.\nLe contenu de cet artiste/publication sera téléchargé dans son sous-dossier spécifique.\nLes filtres (personnage, mots à ignorer, type de fichier) s'appliqueront *à l'intérieur* de chaque dossier d'artiste.\n\nCliquez pour changer pour : Emplacement sélectionné",
"favorite_scope_unknown_text":"Portée : Inconnue",
"favorite_scope_unknown_tooltip":"La portée de téléchargement des favoris est inconnue. Cliquez pour cycler.",
"manga_style_post_title_text":"Nom : Titre de la publication",
"manga_style_original_file_text":"Nom : Fichier original",
"manga_style_date_based_text":"Nom : Basé sur la date",
"manga_style_title_global_num_text":"Nom : Titre+Num.G",
"manga_style_unknown_text":"Nom : Style inconnu",
"fav_artists_dialog_title":"Artistes favoris",
"fav_artists_loading_status":"Chargement des artistes favoris...",
"fav_artists_search_placeholder":"Rechercher des artistes...",
"fav_artists_select_all_button":"Tout sélectionner",
"fav_artists_deselect_all_button":"Tout désélectionner",
"fav_artists_download_selected_button":"Télécharger la sélection",
"fav_artists_cancel_button":"Annuler",
"fav_artists_loading_from_source_status":"⏳ Chargement des favoris depuis {source_name}...",
"fav_artists_found_status":"{count} artiste(s) favori(s) trouvé(s) au total.",
"fav_artists_none_found_status":"Aucun artiste favori trouvé sur Kemono.su ou Coomer.su.",
"fav_artists_failed_status":"Échec de la récupération des favoris.",
"fav_artists_cookies_required_status":"Erreur : Cookies activés mais n'ont pas pu être chargés pour aucune source.",
"fav_artists_no_favorites_after_processing":"Aucun artiste favori trouvé après traitement.",
"fav_artists_no_selection_title":"Aucune sélection",
"fav_artists_no_selection_message":"Veuillez sélectionner au moins un artiste à télécharger.",
"fav_posts_dialog_title":"Publications favorites",
"fav_posts_loading_status":"Chargement des publications favorites...",
"fav_posts_search_placeholder":"Rechercher des publications (titre, créateur, ID, service)...",
"fav_posts_select_all_button":"Tout sélectionner",
"fav_posts_deselect_all_button":"Tout désélectionner",
"fav_posts_download_selected_button":"Télécharger la sélection",
"fav_posts_cancel_button":"Annuler",
"fav_posts_cookies_required_error":"Erreur : Les cookies sont requis pour les publications favorites mais n'ont pas pu être chargés.",
"fav_posts_auth_failed_title":"Échec de l'autorisation (Publications)",
"fav_posts_auth_failed_message":"Impossible de récupérer les favoris{domain_specific_part} en raison d'une erreur d'autorisation :\n\n{error_message}\n\nCela signifie généralement que vos cookies sont manquants, invalides ou expirés pour le site. Veuillez vérifier votre configuration de cookies.",
"fav_posts_fetch_error_title":"Erreur de récupération",
"fav_posts_fetch_error_message":"Erreur lors de la récupération des favoris de {domain}{error_message_part}",
"fav_posts_no_posts_found_status":"Aucune publication favorite trouvée.",
"fav_posts_found_status":"{count} publication(s) favorite(s) trouvée(s).",
"fav_posts_display_error_status":"Erreur d'affichage des publications : {error}",
"fav_posts_ui_error_title":"Erreur d'UI",
"fav_posts_ui_error_message":"Impossible d'afficher les publications favorites : {error}",
"fav_posts_auth_failed_message_generic":"Impossible de récupérer les favoris{domain_specific_part} en raison d'une erreur d'autorisation. Cela signifie généralement que vos cookies sont manquants, invalides ou expirés pour le site. Veuillez vérifier votre configuration de cookies.",
"key_fetching_fav_post_list_init":"Récupération de la liste des publications favorites...",
"key_fetching_from_source_kemono_su":"Récupération des favoris de Kemono.su...",
"key_fetching_from_source_coomer_su":"Récupération des favoris de Coomer.su...",
"fav_posts_fetch_cancelled_status":"Récupération des publications favorites annulée.",
"known_names_filter_dialog_title":"Ajouter des noms connus au filtre",
"known_names_filter_search_placeholder":"Rechercher des noms...",
"known_names_filter_select_all_button":"Tout sélectionner",
"known_names_filter_deselect_all_button":"Tout désélectionner",
"known_names_filter_add_selected_button":"Ajouter la sélection",
"error_files_dialog_title":"Fichiers ignorés en raison d'erreurs",
"error_files_no_errors_label":"Aucun fichier n'a été enregistré comme ignoré en raison d'erreurs lors de la dernière session ou après les nouvelles tentatives.",
"error_files_found_label":"Le(s) {count} fichier(s) suivant(s) a(ont) été ignoré(s) en raison d'erreurs de téléchargement :",
"error_files_select_all_button":"Tout sélectionner",
"error_files_retry_selected_button":"Réessayer la sélection",
"error_files_export_urls_button":"Exporter les URL en .txt",
"error_files_no_selection_retry_message":"Veuillez sélectionner au moins un fichier à réessayer.",
"error_files_no_errors_export_title":"Aucune erreur",
"error_files_no_errors_export_message":"Il n'y a aucune URL de fichier en erreur à exporter.",
"error_files_no_urls_found_export_title":"Aucune URL trouvée",
"error_files_no_urls_found_export_message":"Impossible d'extraire des URL de la liste des fichiers en erreur à exporter.",
"error_files_save_dialog_title":"Enregistrer les URL des fichiers en erreur",
"error_files_export_success_title":"Exportation réussie",
"error_files_export_success_message":"{count} entrées exportées avec succès vers :\n{filepath}",
"error_files_export_error_title":"Erreur d'exportation",
"error_files_export_error_message":"Impossible d'exporter les liens de fichiers : {error}",
"export_options_dialog_title":"Options d'exportation",
"export_options_description_label":"Choisissez le format d'exportation des liens de fichiers en erreur :",
"export_options_radio_link_only":"Lien par ligne (URL uniquement)",
"export_options_radio_link_only_tooltip":"Exporte uniquement l'URL de téléchargement direct pour chaque fichier échoué, une URL par ligne.",
"export_options_radio_with_details":"Exporter avec les détails (URL [Publication, Infos fichier])",
"export_options_radio_with_details_tooltip":"Exporte l'URL suivie de détails comme le titre de la publication, l'ID de la publication et le nom de fichier original entre crochets.",
"export_options_export_button":"Exporter",
"no_errors_logged_title":"Aucune erreur enregistrée",
"no_errors_logged_message":"Aucun fichier n'a été enregistré comme ignoré en raison d'erreurs lors de la dernière session ou après les nouvelles tentatives.",
"progress_initializing_text":"Progression : Initialisation...",
"progress_posts_text":"Progression : {processed_posts} / {total_posts} publications ({progress_percent:.1f}%)",
"progress_processing_post_text":"Progression : Traitement de la publication {processed_posts}...",
"progress_starting_text":"Progression : Démarrage...",
"downloading_file_known_size_text":"Téléchargement de '{filename}' ({downloaded_mb:.1f}Mo / {total_mb:.1f}Mo)",
"downloading_file_unknown_size_text":"Téléchargement de '{filename}' ({downloaded_mb:.1f}Mo)",
"downloading_multipart_text":"DL '{filename}...': {downloaded_mb:.1f}/{total_mb:.1f} Mo ({parts} parties @ {speed:.2f} Mo/s)",
"downloading_multipart_initializing_text":"Fichier : {filename} - Initialisation des parties...",
"status_completed":"Terminé",
"status_cancelled_by_user":"Annulé par l'utilisateur",
"files_downloaded_label":"téléchargés",
"files_skipped_label":"ignorés",
"retry_finished_text":"Nouvelle tentative terminée",
"succeeded_text":"Réussi",
"failed_text":"Échoué",
"ready_for_new_task_text":"Prêt pour une nouvelle tâche.",
"fav_mode_active_label_text":"⭐ Le Mode Favori est actif. Veuillez sélectionner les filtres ci-dessous avant de choisir vos artistes/publications favoris. Sélectionnez une action ci-dessous.",
"export_links_button_text":"Exporter les liens",
"download_extracted_links_button_text":"Télécharger",
"download_selected_button_text":"Télécharger la sélection",
"link_input_placeholder_text":"ex., https://kemono.su/patreon/user/12345 ou .../post/98765",
"link_input_tooltip_text":"Saisissez l'URL complète d'une page de créateur Kemono/Coomer ou d'une publication spécifique.\nExemple (Créateur) : https://kemono.su/patreon/user/12345\nExemple (Publication) : https://kemono.su/patreon/user/12345/post/98765",
"dir_input_placeholder_text":"Sélectionnez le dossier où les téléchargements seront enregistrés",
"dir_input_tooltip_text":"Saisissez ou parcourez jusqu'au dossier principal où tout le contenu téléchargé sera enregistré.\nCeci est requis sauf si le mode 'Liens Uniquement' est sélectionné.",
"character_input_placeholder_text":"ex., Tifa, Aerith, (Cloud, Zack)",
"custom_folder_input_placeholder_text":"Optionnel : Enregistrer cette publication dans un dossier spécifique",
"custom_folder_input_tooltip_text":"Si vous téléchargez une URL de publication unique ET que 'Dossiers séparés par Nom/Titre' est activé,\nvous pouvez saisir un nom personnalisé ici pour le dossier de téléchargement de cette publication.\nExemple : Ma Scène Favorite",
"skip_words_input_placeholder_text":"ex., WM, WIP, sketch, preview",
"remove_from_filename_input_placeholder_text":"ex., patreon, HD",
"cookie_text_input_placeholder_no_file_selected_text":"Chaîne de cookie (si aucun cookies.txt n'est sélectionné)",
"cookie_text_input_placeholder_with_file_selected_text":"Utilisation du fichier de cookie sélectionné (voir Parcourir...)",
"character_search_input_placeholder_text":"Rechercher des personnages...",
"character_search_input_tooltip_text":"Tapez ici pour filtrer la liste des séries/personnages connus ci-dessous.",
"new_char_input_placeholder_text":"Ajouter un nouveau nom de série/personnage",
"new_char_input_tooltip_text":"Saisissez un nouveau nom de série, de jeu ou de personnage à ajouter à la liste ci-dessus.",
"link_search_input_placeholder_text":"Rechercher des liens...",
"link_search_input_tooltip_text":"En mode 'Liens Uniquement', tapez ici pour filtrer les liens affichés par texte, URL ou plateforme.",
"manga_date_prefix_input_placeholder_text":"Préfixe pour les noms de fichiers Manga",
"manga_date_prefix_input_tooltip_text":"Préfixe optionnel pour les noms de fichiers manga 'Basé sur la date' ou 'Fichier original' (ex., 'Nom de la Série').\nSi vide, les fichiers seront nommés en fonction du style sans préfixe.",
"log_display_mode_links_view_text":"🔗 Vue des liens",
"log_display_mode_progress_view_text":"⬇️ Vue de la progression",
"download_external_links_dialog_title":"Télécharger les liens externes sélectionnés",
"select_all_button_text":"Tout sélectionner",
"deselect_all_button_text":"Tout désélectionner",
"cookie_browse_button_tooltip":"Rechercher un fichier de cookie (format Netscape, généralement cookies.txt).\nCelui-ci sera utilisé si 'Utiliser le cookie' est coché et que le champ de texte ci-dessus est vide.",
"page_range_label_text":"Plage de pages :",
"start_page_input_placeholder":"Début",
"start_page_input_tooltip":"Pour les URL de créateurs : Spécifiez le numéro de la page de départ pour le téléchargement (ex., 1, 2, 3).\nLaissez vide ou mettez 1 pour commencer à la première page.\nDésactivé pour les URL de publications uniques ou en Mode Manga/BD.",
"page_range_to_label_text":"à",
"end_page_input_placeholder":"Fin",
"end_page_input_tooltip":"Pour les URL de créateurs : Spécifiez le numéro de la page de fin pour le téléchargement (ex., 5, 10).\nLaissez vide pour télécharger toutes les pages à partir de la page de départ.\nDésactivé pour les URL de publications uniques ou en Mode Manga/BD.",
"known_names_help_button_tooltip_text":"Ouvrir le guide des fonctionnalités de l'application.",
"future_settings_button_tooltip_text":"Ouvrir les paramètres de l'application (Thème, Langue, etc.).",
"link_search_button_tooltip_text":"Filtrer les liens affichés",
"confirm_add_all_dialog_title":"Confirmer l'ajout de nouveaux noms",
"confirm_add_all_info_label":"Les nouveaux noms/groupes suivants de votre entrée 'Filtrer par Personnage(s)' ne sont pas dans 'Known.txt'.\nLeur ajout peut améliorer l'organisation des dossiers pour les futurs téléchargements.\n\nVeuillez examiner la liste et choisir une action :",
"confirm_add_all_select_all_button":"Tout sélectionner",
"confirm_add_all_deselect_all_button":"Tout désélectionner",
"confirm_add_all_add_selected_button":"Ajouter la sélection à Known.txt",
"confirm_add_all_skip_adding_button":"Ignorer l'ajout de ceux-ci",
"confirm_add_all_cancel_download_button":"Annuler le téléchargement",
"cookie_help_dialog_title":"Instructions pour le fichier de cookies",
"cookie_help_instruction_intro":"<p>Pour utiliser les cookies, vous avez généralement besoin d'un fichier <b>cookies.txt</b> de votre navigateur.</p>",
"cookie_help_how_to_get_title":"<p><b>Comment obtenir cookies.txt :</b></p>",
"cookie_help_step1_extension_intro":"<li>Installez l'extension 'Get cookies.txt LOCALLY' pour votre navigateur basé sur Chrome :<br><a href=\"https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc\" style=\"color: #87CEEB;\">Get cookies.txt LOCALLY sur le Chrome Web Store</a></li>",
"cookie_help_step2_login":"<li>Allez sur le site web (ex., kemono.su ou coomer.su) et connectez-vous si nécessaire.</li>",
"cookie_help_step3_click_icon":"<li>Cliquez sur l'icône de l'extension dans la barre d'outils de votre navigateur.</li>",
"cookie_help_step4_export":"<li>Cliquez sur un bouton 'Exporter' (ex., \"Exporter sous\", \"Exporter cookies.txt\" - le libellé exact peut varier selon la version de l'extension).</li>",
"cookie_help_step5_save_file":"<li>Enregistrez le fichier <code>cookies.txt</code> téléchargé sur votre ordinateur.</li>",
"cookie_help_step6_app_intro":"<li>Dans cette application :<ul>",
"cookie_help_step6a_checkbox":"<li>Assurez-vous que la case 'Utiliser le cookie' est cochée.</li>",
"cookie_help_step6b_browse":"<li>Cliquez sur le bouton 'Parcourir...' à côté du champ de texte du cookie.</li>",
"cookie_help_step6c_select":"<li>Sélectionnez le fichier <code>cookies.txt</code> que vous venez d'enregistrer.</li></ul></li>",
"cookie_help_alternative_paste":"<p>Alternativement, certaines extensions peuvent vous permettre de copier la chaîne de cookie directement. Si c'est le cas, vous pouvez la coller dans le champ de texte au lieu de rechercher un fichier.</p>",
"cookie_help_proceed_without_button":"Télécharger sans cookies",
"cookie_help_cancel_download_button":"Annuler le téléchargement", # FR_ADD_KEY_HERE
"empty_popup_button_tooltip_text": "Ouvrir la sélection du créateur (Parcourir creators.json)",
"character_input_tooltip":"Saisissez les noms des personnages (séparés par des virgules). Prend en charge le groupement avancé et affecte le nommage des dossiers si 'Dossiers séparés' est activé.\n\nExemples :\n- Nami → Correspond à 'Nami', crée le dossier 'Nami'.\n- (Ulti, Vivi) → Correspond à l'un ou l'autre, dossier 'Ulti Vivi', ajoute les deux à Known.txt séparément.\n- (Boa, Hancock)~ → Correspond à l'un ou l'autre, dossier 'Boa Hancock', ajoute comme un seul groupe dans Known.txt.\n\nLes noms sont traités comme des alias pour la correspondance.\n\nModes de filtre (le bouton cycle) :\n- Fichiers : Filtre par nom de fichier.\n- Titre : Filtre par titre de publication.\n- Les deux : Titre d'abord, puis nom de fichier.\n- Commentaires (Bêta) : Nom de fichier d'abord, puis commentaires de la publication.",
"tour_dialog_title":"Bienvenue dans Kemono Downloader !",
"tour_dialog_never_show_checkbox":"Ne plus jamais afficher cette visite",
"tour_dialog_skip_button":"Passer la visite",
"tour_dialog_back_button":"Retour",
"tour_dialog_next_button":"Suivant",
"tour_dialog_finish_button":"Terminer",
"tour_dialog_step1_title":"👋 Bienvenue !",
"tour_dialog_step1_content":"Bonjour ! Cette visite rapide vous guidera à travers les principales fonctionnalités de Kemono Downloader, y compris les mises à jour récentes comme le filtrage amélioré, les améliorations du mode manga et la gestion des cookies.\n<ul>\n<li>Mon objectif est de vous aider à télécharger facilement du contenu de <b>Kemono</b> et <b>Coomer</b>.</li><br>\n<li><b>🎨 Bouton de sélection du créateur :</b> À côté de la saisie de l'URL, cliquez sur l'icône de la palette pour ouvrir une boîte de dialogue. Parcourez et sélectionnez les créateurs de votre fichier <code>creators.json</code> pour ajouter rapidement leurs noms à la saisie de l'URL.</li><br>\n<li><b>Conseil important : L'application '(Ne répond pas)' ?</b><br>\nAprès avoir cliqué sur 'Démarrer le téléchargement', en particulier pour les grands flux de créateurs ou avec de nombreux threads, l'application peut temporairement afficher '(Ne répond pas)'. Votre système d'exploitation (Windows, macOS, Linux) pourrait même vous suggérer de 'Terminer le processus' ou de 'Forcer à quitter'.<br>\n<b>Veuillez être patient !</b> L'application travaille souvent d'arrache-pied en arrière-plan. Avant de forcer la fermeture, essayez de vérifier votre 'Emplacement de téléchargement' choisi dans votre explorateur de fichiers. Si vous voyez de nouveaux dossiers se créer ou des fichiers apparaître, cela signifie que le téléchargement progresse correctement. Donnez-lui un peu de temps pour redevenir réactif.</li><br>\n<li>Utilisez les boutons <b>Suivant</b> et <b>Retour</b> pour naviguer.</li><br>\n<li>De nombreuses options ont des info-bulles si vous les survolez pour plus de détails.</li><br>\n<li>Cliquez sur <b>Passer la visite</b> pour fermer ce guide à tout moment.</li><br>\n<li>Cochez <b>'Ne plus jamais afficher cette visite'</b> si vous ne voulez pas voir cela lors des démarrages futurs.</li>\n</ul>",
"tour_dialog_step2_title":"① Pour commencer",
"tour_dialog_step2_content":"Commençons par les bases du téléchargement :\n<ul>\n<li><b>🔗 URL Créateur/Post Kemono :</b><br>\nCollez l'adresse web complète (URL) de la page d'un créateur (par ex., <i>https://kemono.su/patreon/user/12345</i>) \nou d'une publication spécifique (par ex., <i>.../post/98765</i>).<br>\nou d'un créateur Coomer (par ex., <i>https://coomer.su/onlyfans/user/artistname</i>)</li><br>\n<li><b>📁 Emplacement de téléchargement :</b><br>\nCliquez sur 'Parcourir...' pour choisir un dossier sur votre ordinateur où tous les fichiers téléchargés seront enregistrés. \nCeci est requis sauf si vous utilisez le mode 'Liens Uniquement'.</li><br>\n<li><b>📄 Plage de pages (URL de créateur uniquement) :</b><br>\nSi vous téléchargez depuis la page d'un créateur, vous pouvez spécifier une plage de pages à récupérer (par ex., pages 2 à 5). \nLaissez vide pour toutes les pages. Ceci est désactivé pour les URL de publications uniques ou lorsque le <b>Mode Manga/BD</b> est actif.</li>\n</ul>",
"tour_dialog_step3_title":"② Filtrage des téléchargements",
"tour_dialog_step3_content":"Affinez ce que vous téléchargez avec ces filtres (la plupart sont désactivés en modes 'Liens Uniquement' ou 'Archives Uniquement') :\n<ul>\n<li><b>🎯 Filtrer par Personnage(s) :</b><br>\nSaisissez les noms des personnages, séparés par des virgules (par ex., <i>Tifa, Aerith</i>). Groupez les alias pour un nom de dossier combiné : <i>(alias1, alias2, alias3)</i> devient le dossier 'alias1 alias2 alias3' (après nettoyage). Tous les noms du groupe sont utilisés comme alias pour la correspondance.<br>\nLe bouton <b>'Filtre : [Type]'</b> (à côté de cette entrée) change la façon dont ce filtre s'applique :\n<ul><li><i>Filtre : Fichiers :</i> Vérifie les noms de fichiers individuels. Une publication est conservée si un fichier correspond ; seuls les fichiers correspondants sont téléchargés. Le nommage du dossier utilise le personnage du nom de fichier correspondant (si 'Dossiers séparés' est activé).</li><br>\n<li><i>Filtre : Titre :</i> Vérifie les titres des publications. Tous les fichiers d'une publication correspondante sont téléchargés. Le nommage du dossier utilise le personnage du titre de la publication correspondante.</li>\n<li><b>⤵️ Bouton Ajouter au filtre (Noms connus) :</b> À côté du bouton 'Ajouter' pour les Noms connus (voir Étape 5), cela ouvre une popup. Sélectionnez les noms de votre liste <code>Known.txt</code> via des cases à cocher (avec une barre de recherche) pour les ajouter rapidement au champ 'Filtrer par Personnage(s)'. Les noms groupés comme <code>(Boa, Hancock)</code> de Known.txt seront ajoutés comme <code>(Boa, Hancock)~</code> au filtre.</li><br>\n<li><i>Filtre : Les deux :</i> Vérifie d'abord le titre de la publication. S'il correspond, tous les fichiers sont téléchargés. Sinon, il vérifie ensuite les noms de fichiers, et seuls les fichiers correspondants sont téléchargés. Le nommage du dossier priorise la correspondance de titre, puis la correspondance de fichier.</li><br>\n<li><i>Filtre : Commentaires (Bêta) :</i> Vérifie d'abord les noms de fichiers. Si un fichier correspond, tous les fichiers de la publication sont téléchargés. Si aucune correspondance de fichier, il vérifie alors les commentaires de la publication. Si un commentaire correspond, tous les fichiers sont téléchargés. (Utilise plus de requêtes API). Le nommage du dossier priorise la correspondance de fichier, puis la correspondance de commentaire.</li></ul>\nCe filtre influence également le nommage des dossiers si 'Dossiers séparés par Nom/Titre' est activé.</li><br>\n<li><b>🚫 Ignorer avec les mots :</b><br>\nSaisissez des mots, séparés par des virgules (par ex., <i>WIP, sketch, preview</i>). \nLe bouton <b>'Portée : [Type]'</b> (à côté de cette entrée) change la façon dont ce filtre s'applique :\n<ul><li><i>Portée : Fichiers :</i> Ignore les fichiers si leurs noms contiennent l'un de ces mots.</li><br>\n<li><i>Portée : Publications :</i> Ignore les publications entières si leurs titres contiennent l'un de ces mots.</li><br>\n<li><i>Portée : Les deux :</i> Applique à la fois l'omission par titre de fichier et de publication (publication d'abord, puis fichiers).</li></ul></li><br>\n<li><b>Filtrer les fichiers (Boutons radio) :</b> Choisissez ce qu'il faut télécharger :\n<ul>\n<li><i>Tout :</i> Télécharge tous les types de fichiers trouvés.</li><br>\n<li><i>Images/GIFs :</i> Uniquement les formats d'image courants et les GIFs.</li><br>\n<li><i>Vidéos :</i> Uniquement les formats vidéo courants.</li><br>\n<li><b><i>📦 Archives Uniquement :</i></b> Télécharge exclusivement les fichiers <b>.zip</b> et <b>.rar</b>. Lorsque cette option est sélectionnée, les cases à cocher 'Ignorer .zip' et 'Ignorer .rar' sont automatiquement désactivées et décochées. 'Afficher les liens externes' est également désactivé.</li><br>\n<li><i>🎧 Audio Uniquement :</i> Uniquement les formats audio courants (MP3, WAV, FLAC, etc.).</li><br>\n<li><i>🔗 Liens Uniquement :</i> Extrait et affiche les liens externes des descriptions de publications au lieu de télécharger des fichiers. Les options liées au téléchargement et 'Afficher les liens externes' sont désactivées.</li>\n</ul></li>\n</ul>",
"tour_dialog_step4_title":"③ Mode Favori (Téléchargement alternatif)",
"tour_dialog_step4_content":"L'application propose un 'Mode Favori' pour télécharger du contenu d'artistes que vous avez mis en favoris sur Kemono.su.\n<ul>\n<li><b>⭐ Case à cocher Mode Favori :</b><br>\nSituée à côté du bouton radio '🔗 Liens Uniquement'. Cochez cette case pour activer le Mode Favori.</li><br>\n<li><b>Que se passe-t-il en Mode Favori :</b>\n<ul><li>La zone de saisie '🔗 URL Créateur/Post Kemono' est remplacée par un message indiquant que le Mode Favori est actif.</li><br>\n<li>Les boutons standard 'Démarrer le téléchargement', 'Pause', 'Annuler' sont remplacés par les boutons '🖼️ Artistes favoris' et '📄 Publications favorites' (Note : 'Publications favorites' est prévu pour le futur).</li><br>\n<li>L'option '🍪 Utiliser le cookie' est automatiquement activée et verrouillée, car les cookies sont nécessaires pour récupérer vos favoris.</li></ul></li><br>\n<li><b>🖼️ Bouton Artistes favoris :</b><br>\nCliquez ici pour ouvrir une boîte de dialogue listant vos artistes favoris de Kemono.su. Vous pouvez sélectionner un ou plusieurs artistes à télécharger.</li><br>\n<li><b>Portée de téléchargement des favoris (Bouton) :</b><br>\nCe bouton (à côté de 'Publications favorites') contrôle où les favoris sélectionnés sont téléchargés :\n<ul><li><i>Portée : Emplacement sélectionné :</i> Tous les artistes sélectionnés sont téléchargés dans l' 'Emplacement de téléchargement' principal que vous avez défini. Les filtres s'appliquent globalement.</li><br>\n<li><i>Portée : Dossiers d'artistes :</i> Un sous-dossier (nommé d'après l'artiste) est créé dans votre 'Emplacement de téléchargement' principal pour chaque artiste sélectionné. Le contenu de cet artiste va dans son dossier spécifique. Les filtres s'appliquent à l'intérieur de chaque dossier d'artiste.</li></ul></li><br>\n<li><b>Filtres en Mode Favori :</b><br>\nLes options 'Filtrer par Personnage(s)', 'Ignorer avec les mots' et 'Filtrer les fichiers' s'appliquent toujours au contenu téléchargé de vos artistes favoris sélectionnés.</li>\n</ul>",
"tour_dialog_step5_title":"④ Affiner les téléchargements",
"tour_dialog_step5_content":"Plus d'options pour personnaliser vos téléchargements :\n<ul>\n<li><b>Ignorer .zip / Ignorer .rar :</b> Cochez ces cases pour éviter de télécharger ces types de fichiers d'archive. \n<i>(Note : Celles-ci sont désactivées et ignorées si le mode de filtre '📦 Archives Uniquement' est sélectionné).</i></li><br>\n<li><b>✂️ Supprimer les mots du nom :</b><br>\nSaisissez des mots, séparés par des virgules (par ex., <i>patreon, [HD]</i>), à supprimer des noms de fichiers téléchargés (insensible à la casse).</li><br>\n<li><b>Télécharger les miniatures uniquement :</b> Télécharge les petites images d'aperçu au lieu des fichiers en taille réelle (si disponible).</li><br>\n<li><b>Compresser les grandes images :</b> Si la bibliothèque 'Pillow' est installée, les images de plus de 1.5 Mo seront converties au format WebP si la version WebP est significativement plus petite.</li><br>\n<li><b>🗄️ Nom de dossier personnalisé (Publication unique uniquement) :</b><br>\nSi vous téléchargez une URL de publication spécifique ET que 'Dossiers séparés par Nom/Titre' est activé, \nvous pouvez saisir un nom personnalisé ici pour le dossier de téléchargement de cette publication.</li><br>\n<li><b>🍪 Utiliser le cookie :</b> Cochez cette case pour utiliser des cookies pour les requêtes. Vous pouvez soit :\n<ul><li>Saisir une chaîne de cookie directement dans le champ de texte (par ex., <i>nom1=valeur1; nom2=valeur2</i>).</li><br>\n<li>Cliquer sur 'Parcourir...' pour sélectionner un fichier <i>cookies.txt</i> (format Netscape). Le chemin apparaîtra dans le champ de texte.</li></ul>\nCeci est utile pour accéder au contenu qui nécessite une connexion. Le champ de texte a la priorité s'il est rempli. \nSi 'Utiliser le cookie' est coché mais que le champ de texte et le fichier parcouru sont vides, il essaiera de charger 'cookies.txt' depuis le répertoire de l'application.</li>\n</ul>",
"tour_dialog_step6_title":"⑤ Organisation & Performance",
"tour_dialog_step6_content":"Organisez vos téléchargements et gérez les performances :\n<ul>\n<li><b>⚙️ Dossiers séparés par Nom/Titre :</b> Crée des sous-dossiers basés sur l'entrée 'Filtrer par Personnage(s)' ou les titres des publications (peut utiliser la liste <b>Known.txt</b> comme solution de repli pour les noms de dossiers).</li><br>\n<li><b>Sous-dossier par publication :</b> Si 'Dossiers séparés' est activé, cela crée un sous-dossier supplémentaire pour <i>chaque publication individuelle</i> à l'intérieur du dossier principal personnage/titre.</li><br>\n<li><b>🚀 Utiliser le multithreading (Threads) :</b> Active des opérations plus rapides. Le nombre dans l'entrée 'Threads' signifie :\n<ul><li>Pour les <b>Flux de créateurs :</b> Nombre de publications à traiter simultanément. Les fichiers de chaque publication sont téléchargés séquentiellement par son worker (sauf si le nommage de manga 'Basé sur la date' est activé, ce qui force 1 worker de publication).</li><br>\n<li>Pour les <b>URL de publications uniques :</b> Nombre de fichiers à télécharger simultanément à partir de cette seule publication.</li></ul>\nSi décoché, 1 thread est utilisé. Des nombres élevés de threads (par ex., >40) peuvent afficher un avertissement.</li><br>\n<li><b>Bascule de téléchargement multi-partie (en haut à droite de la zone du journal) :</b><br>\nLe bouton <b>'Multi-partie : [ON/OFF]'</b> permet d'activer/désactiver les téléchargements multi-segments pour les fichiers volumineux individuels. \n<ul><li><b>ON :</b> Peut accélérer les téléchargements de fichiers volumineux (par ex., des vidéos) mais peut augmenter les saccades de l'UI ou le spam du journal avec de nombreux petits fichiers. Un avertissement apparaîtra lors de l'activation. Si un téléchargement multi-partie échoue, il réessaie en flux unique.</li><br>\n<li><b>OFF (Défaut) :</b> Les fichiers sont téléchargés en un seul flux.</li></ul>\nCeci est désactivé si le mode 'Liens Uniquement' ou 'Archives Uniquement' est actif.</li><br>\n<li><b>📖 Mode Manga/BD (URL de créateur uniquement) :</b> Conçu pour le contenu séquentiel.\n<ul>\n<li>Télécharge les publications du <b>plus ancien au plus récent</b>.</li><br>\n<li>L'entrée 'Plage de pages' est désactivée car toutes les publications sont récupérées.</li><br>\n<li>Un <b>bouton de bascule de style de nom de fichier</b> (par ex., 'Nom : Titre de la publication') apparaît en haut à droite de la zone du journal lorsque ce mode est actif pour un flux de créateur. Cliquez dessus pour cycler entre les styles de nommage :\n<ul>\n<li><b><i>Nom : Titre de la publication (Défaut) :</i></b> Le premier fichier d'une publication est nommé d'après le titre nettoyé de la publication (par ex., 'Mon Chapitre 1.jpg'). Les fichiers suivants dans la *même publication* tenteront de conserver leurs noms de fichiers originaux (par ex., 'page_02.png', 'bonus_art.jpg'). Si la publication n'a qu'un seul fichier, il est nommé d'après le titre de la publication. C'est généralement recommandé pour la plupart des mangas/BD.</li><br>\n<li><b><i>Nom : Fichier original :</i></b> Tous les fichiers tentent de conserver leurs noms de fichiers originaux. Un préfixe optionnel (par ex., 'MaSerie_') peut être saisi dans le champ de saisie qui apparaît à côté du bouton de style. Exemple : 'MaSerie_FichierOriginal.jpg'.</li><br>\n<li><b><i>Nom : Titre+Num.G (Titre de la publication + Numérotation globale) :</i></b> Tous les fichiers de toutes les publications de la session de téléchargement actuelle sont nommés séquentiellement en utilisant le titre nettoyé de la publication comme préfixe, suivi d'un compteur global. Par exemple : Publication 'Chapitre 1' (2 fichiers) -> 'Chapitre 1_001.jpg', 'Chapitre 1_002.png'. La publication suivante, 'Chapitre 2' (1 fichier), continuerait la numérotation -> 'Chapitre 2_003.jpg'. Le multithreading pour le traitement des publications est automatiquement désactivé pour ce style afin d'assurer une numérotation globale correcte.</li><br>\n<li><b><i>Nom : Basé sur la date :</i></b> Les fichiers sont nommés séquentiellement (001.ext, 002.ext, ...) en fonction de l'ordre de publication des publications. Un préfixe optionnel (par ex., 'MaSerie_') peut être saisi dans le champ de saisie qui apparaît à côté du bouton de style. Exemple : 'MaSerie_001.jpg'. Le multithreading pour le traitement des publications est automatiquement désactivé pour ce style.</li>\n</ul>\n</li><br>\n<li>Pour de meilleurs résultats avec les styles 'Nom : Titre de la publication', 'Nom : Titre+Num.G' ou 'Nom : Basé sur la date', utilisez le champ 'Filtrer par Personnage(s)' avec le titre du manga/de la série pour l'organisation des dossiers.</li>\n</ul></li><br>\n<li><b>🎭 Known.txt pour une organisation intelligente des dossiers :</b><br>\n<code>Known.txt</code> (dans le répertoire de l'application) permet un contrôle fin de l'organisation automatique des dossiers lorsque 'Dossiers séparés par Nom/Titre' est actif.\n<ul>\n<li><b>Comment ça marche :</b> Chaque ligne de <code>Known.txt</code> est une entrée. \n<ul><li>Une ligne simple comme <code>Ma Super Série</code> signifie que le contenu correspondant ira dans un dossier nommé \"Ma Super Série\".</li><br>\n<li>Une ligne groupée comme <code>(Personnage A, Perso A, Nom Alt A)</code> signifie que le contenu correspondant à \"Personnage A\", \"Perso A\", OU \"Nom Alt A\" ira TOUS dans un seul dossier nommé \"Personnage A Perso A Nom Alt A\" (après nettoyage). Tous les termes entre parenthèses deviennent des alias pour ce dossier.</li></ul></li>\n<li><b>Repli intelligent :</b> Lorsque 'Dossiers séparés par Nom/Titre' est actif, et si une publication ne correspond à aucune entrée spécifique 'Filtrer par Personnage(s)', le téléchargeur consulte <code>Known.txt</code> pour trouver un nom principal correspondant pour la création du dossier.</li><br>\n<li><b>Gestion conviviale :</b> Ajoutez des noms simples (non groupés) via la liste de l'UI ci-dessous. Pour une édition avancée (comme la création/modification d'alias groupés), cliquez sur <b>'Ouvrir Known.txt'</b> pour éditer le fichier dans votre éditeur de texte. L'application le recharge à la prochaine utilisation ou au prochain démarrage.</li>\n</ul>\n</li>\n</ul>",
"tour_dialog_step7_title":"⑥ Erreurs courantes & Dépannage",
"tour_dialog_step7_content":"Parfois, les téléchargements peuvent rencontrer des problèmes. Voici quelques-uns des plus courants :\n<ul>\n<li><b>Info-bulle de saisie de personnage :</b><br>\nSaisissez les noms des personnages, séparés par des virgules (par ex., <i>Tifa, Aerith</i>).<br>\nGroupez les alias pour un nom de dossier combiné : <i>(alias1, alias2, alias3)</i> devient le dossier 'alias1 alias2 alias3'.<br>\nTous les noms du groupe sont utilisés comme alias pour la correspondance de contenu.<br><br>\nLe bouton 'Filtre : [Type]' à côté de cette entrée change la façon dont ce filtre s'applique :<br>\n- Filtre : Fichiers : Vérifie les noms de fichiers individuels. Seuls les fichiers correspondants sont téléchargés.<br>\n- Filtre : Titre : Vérifie les titres des publications. Tous les fichiers d'une publication correspondante sont téléchargés.<br>\n- Filtre : Les deux : Vérifie d'abord le titre de la publication. Si aucune correspondance, vérifie ensuite les noms de fichiers.<br>\n- Filtre : Commentaires (Bêta) : Vérifie d'abord les noms de fichiers. Si aucune correspondance, vérifie ensuite les commentaires de la publication.<br><br>\nCe filtre influence également le nommage des dossiers si 'Dossiers séparés par Nom/Titre' est activé.</li><br>\n<li><b>502 Bad Gateway / 503 Service Unavailable / 504 Gateway Timeout :</b><br>\nCeux-ci indiquent généralement des problèmes temporaires côté serveur avec Kemono/Coomer. Le site peut être surchargé, en maintenance ou rencontrer des problèmes. <br>\n<b>Solution :</b> Attendez un peu (par ex., 30 minutes à quelques heures) et réessayez plus tard. Vérifiez le site directement dans votre navigateur.</li><br>\n<li><b>Connexion perdue / Connexion refusée / Timeout (pendant le téléchargement de fichier) :</b><br>\nCela peut arriver à cause de votre connexion internet, de l'instabilité du serveur, ou si le serveur interrompt la connexion pour un fichier volumineux. <br>\n<b>Solution :</b> Vérifiez votre internet. Essayez de réduire le nombre de 'Threads' s'il est élevé. L'application pourrait proposer de réessayer certains fichiers échoués à la fin d'une session.</li><br>\n<li><b>Erreur IncompleteRead :</b><br>\nLe serveur a envoyé moins de données que prévu. Souvent un problème réseau temporaire ou un problème de serveur. <br>\n<b>Solution :</b> L'application marquera souvent ces fichiers pour une nouvelle tentative à la fin de la session de téléchargement.</li><br>\n<li><b>403 Forbidden / 401 Unauthorized (moins courant pour les publications publiques) :</b><br>\nVous n'avez peut-être pas la permission d'accéder au contenu. Pour certains contenus payants ou privés, l'utilisation de l'option 'Utiliser le cookie' avec des cookies valides de votre session de navigateur pourrait aider. Assurez-vous que vos cookies sont à jour.</li><br>\n<li><b>404 Not Found :</b><br>\nL'URL de la publication ou du fichier est incorrecte, ou le contenu a été supprimé du site. Vérifiez l'URL.</li><br>\n<li><b>'Aucune publication trouvée' / 'Publication cible non trouvée' :</b><br>\nAssurez-vous que l'URL est correcte et que le créateur/la publication existe. Si vous utilisez des plages de pages, assurez-vous qu'elles sont valides pour le créateur. Pour les publications très récentes, il peut y avoir un léger délai avant qu'elles n'apparaissent dans l'API.</li><br>\n<li><b>Lenteur générale / Application '(Ne répond pas)' :</b><br>\nComme mentionné à l'étape 1, si l'application semble se bloquer après le démarrage, en particulier avec de grands flux de créateurs ou de nombreux threads, veuillez lui donner du temps. Elle traite probablement des données en arrière-plan. Réduire le nombre de threads peut parfois améliorer la réactivité si cela est fréquent.</li>\n</ul>",
"tour_dialog_step8_title":"⑦ Journaux & Contrôles finaux",
"tour_dialog_step8_content":"Surveillance et Contrôles :\n<ul>\n<li><b>📜 Journal de progression / Journal des liens extraits :</b> Affiche les messages de téléchargement détaillés. Si le mode '🔗 Liens Uniquement' est actif, cette zone affiche les liens extraits.</li><br>\n<li><b>Afficher les liens externes dans le journal :</b> Si coché, un panneau de journal secondaire apparaît sous le journal principal pour afficher les liens externes trouvés dans les descriptions de publications. <i>(Ceci est désactivé si le mode '🔗 Liens Uniquement' ou '📦 Archives Uniquement' est actif).</i></li><br>\n<li><b>Bascule d'affichage du journal (Bouton 👁️ / 🙈) :</b><br>\nCe bouton (en haut à droite de la zone du journal) change la vue du journal principal :\n<ul><li><b>👁️ Journal de progression (Défaut) :</b> Affiche toute l'activité de téléchargement, les erreurs et les résumés.</li><br>\n<li><b>🙈 Journal des personnages manqués :</b> Affiche une liste de termes clés des titres de publications qui ont été ignorés en raison de vos paramètres 'Filtrer par Personnage(s)'. Utile pour identifier le contenu que vous pourriez manquer involontairement.</li></ul></li><br>\n<li><b>🔄 Réinitialiser :</b> Efface tous les champs de saisie, les journaux et réinitialise les paramètres temporaires à leurs valeurs par défaut. Ne peut être utilisé que lorsqu'aucun téléchargement n'est actif.</li><br>\n<li><b>⬇️ Démarrer le téléchargement / 🔗 Extraire les liens / ⏸️ Pause / ❌ Annuler :</b> Ces boutons contrôlent le processus. 'Annuler & Réinitialiser l'UI' arrête l'opération en cours et effectue une réinitialisation logicielle de l'UI, en conservant vos entrées d'URL et de répertoire. 'Pause/Reprendre' permet d'arrêter temporairement et de continuer.</li><br>\n<li>Si certains fichiers échouent avec des erreurs récupérables (comme 'IncompleteRead'), il se peut que l'on vous propose de les réessayer à la fin d'une session.</li>\n</ul>\n<br>Vous êtes prêt ! Cliquez sur <b>'Terminer'</b> pour fermer la visite et commencer à utiliser le téléchargeur.",
"help_guide_dialog_title":"Kemono Downloader - Guide des fonctionnalités",
"help_guide_github_tooltip":"Visiter la page GitHub du projet (S'ouvre dans le navigateur)",
"help_guide_instagram_tooltip":"Visiter notre page Instagram (S'ouvre dans le navigateur)",
"help_guide_discord_tooltip":"Rejoindre notre communauté Discord (S'ouvre dans le navigateur)",
"help_guide_step1_title":"① Introduction & Entrées principales",
"help_guide_step1_content":"<html><head/><body>\n<p>Ce guide offre un aperçu des fonctionnalités, des champs et des boutons de Kemono Downloader.</p>\n<h3>Zone de saisie principale (en haut à gauche)</h3>\n<ul>\n<li><b>🔗 URL Créateur/Post Kemono :</b>\n<ul>\n<li>Saisissez l'adresse web complète de la page d'un créateur (par ex., <i>https://kemono.su/patreon/user/12345</i>) ou d'une publication spécifique (par ex., <i>.../post/98765</i>).</li>\n<li>Prend en charge les URL de Kemono (kemono.su, kemono.party) et Coomer (coomer.su, coomer.party).</li>\n</ul>\n</li>\n<li><b>Plage de pages (Début à Fin) :</b>\n<ul>\n<li>Pour les URL de créateurs : Spécifiez une plage de pages à récupérer (par ex., pages 2 à 5). Laissez vide pour toutes les pages.</li>\n<li>Désactivé pour les URL de publications uniques ou lorsque le <b>Mode Manga/BD</b> est actif.</li>\n</ul>\n</li>\n<li><b>📁 Emplacement de téléchargement :</b>\n<ul>\n<li>Cliquez sur <b>'Parcourir...'</b> pour choisir un dossier principal sur votre ordinateur où tous les fichiers téléchargés seront enregistrés.</li>\n<li>Ce champ est requis sauf si vous utilisez le mode <b>'🔗 Liens Uniquement'</b>.</li>\n</ul>\n</li>\n<li><b>🎨 Bouton de sélection du créateur (à côté de la saisie de l'URL) :</b>\n<ul>\n<li>Cliquez sur l'icône de la palette (🎨) pour ouvrir la boîte de dialogue 'Sélection du créateur'.</li>\n<li>Cette boîte de dialogue charge les créateurs depuis votre fichier <code>creators.json</code> (qui doit se trouver dans le répertoire de l'application).</li>\n<li><b>À l'intérieur de la boîte de dialogue :</b>\n<ul>\n<li><b>Barre de recherche :</b> Tapez pour filtrer la liste des créateurs par nom ou service.</li>\n<li><b>Liste des créateurs :</b> Affiche les créateurs de votre <code>creators.json</code>. Les créateurs que vous avez mis en 'favoris' (dans les données JSON) apparaissent en haut.</li>\n<li><b>Cases à cocher :</b> Sélectionnez un ou plusieurs créateurs en cochant la case à côté de leur nom.</li>\n<li><b>Bouton 'Portée' (par ex., 'Portée : Personnages') :</b> Ce bouton bascule l'organisation du téléchargement lors de l'initiation des téléchargements à partir de cette popup :\n<ul><li><i>Portée : Personnages :</i> Les téléchargements seront organisés dans des dossiers nommés d'après les personnages directement dans votre 'Emplacement de téléchargement' principal. Les œuvres de différents créateurs pour le même personnage seront regroupées.</li>\n<li><i>Portée : Créateurs :</i> Les téléchargements créeront d'abord un dossier nommé d'après le créateur dans votre 'Emplacement de téléchargement' principal. Les sous-dossiers nommés d'après les personnages seront ensuite créés à l'intérieur du dossier de chaque créateur.</li></ul>\n</li>\n<li><b>Bouton 'Ajouter la sélection' :</b> Cliquer sur ce bouton prendra les noms de tous les créateurs cochés et les ajoutera au champ de saisie principal '🔗 URL Créateur/Post Kemono', séparés par des virgules. La boîte de dialogue se fermera alors.</li>\n</ul>\n</li>\n<li>Cette fonctionnalité offre un moyen rapide de remplir le champ URL pour plusieurs créateurs sans avoir à taper ou coller manuellement chaque URL.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step2_title":"② Filtrage des téléchargements",
"help_guide_step2_content":"<html><head/><body>\n<h3>Filtrage des téléchargements (Panneau de gauche)</h3>\n<ul>\n<li><b>🎯 Filtrer par Personnage(s) :</b>\n<ul>\n<li>Saisissez les noms, séparés par des virgules (par ex., <code>Tifa, Aerith</code>).</li>\n<li><b>Alias groupés pour dossier partagé (Entrées Known.txt séparées) :</b> <code>(Vivi, Ulti, Uta)</code>.\n<ul><li>Le contenu correspondant à \"Vivi\", \"Ulti\", OU \"Uta\" ira dans un dossier partagé nommé \"Vivi Ulti Uta\" (après nettoyage).</li>\n<li>Si ces noms sont nouveaux, il vous sera demandé d'ajouter \"Vivi\", \"Ulti\" et \"Uta\" comme des <i>entrées individuelles séparées</i> à <code>Known.txt</code>.</li>\n</ul>\n</li>\n<li><b>Alias groupés pour dossier partagé (Entrée Known.txt unique) :</b> <code>(Yuffie, Sonon)~</code> (notez le tilde <code>~</code>).\n<ul><li>Le contenu correspondant à \"Yuffie\" OU \"Sonon\" ira dans un dossier partagé nommé \"Yuffie Sonon\".</li>\n<li>Si nouveau, \"Yuffie Sonon\" (avec les alias Yuffie, Sonon) sera proposé pour être ajouté comme une <i>entrée de groupe unique</i> à <code>Known.txt</code>.</li>\n</ul>\n</li>\n<li>Ce filtre influence le nommage des dossiers si 'Dossiers séparés par Nom/Titre' est activé.</li>\n</ul>\n</li>\n<li><b>Filtre : Bouton [Type] (Portée du filtre de personnage) :</b> Cycle la façon dont le 'Filtrer par Personnage(s)' s'applique :\n<ul>\n<li><code>Filtre : Fichiers</code> : Vérifie les noms de fichiers individuels. Une publication est conservée si un fichier correspond ; seuls les fichiers correspondants sont téléchargés. Le nommage du dossier utilise le personnage du nom de fichier correspondant.</li>\n<li><code>Filtre : Titre</code> : Vérifie les titres des publications. Tous les fichiers d'une publication correspondante sont téléchargés. Le nommage du dossier utilise le personnage du titre de la publication correspondante.</li>\n<li><code>Filtre : Les deux</code> : Vérifie d'abord le titre de la publication. S'il correspond, tous les fichiers sont téléchargés. Sinon, il vérifie ensuite les noms de fichiers, et seuls les fichiers correspondants sont téléchargés. Le nommage du dossier priorise la correspondance de titre, puis la correspondance de fichier.</li>\n<li><code>Filtre : Commentaires (Bêta)</code> : Vérifie d'abord les noms de fichiers. Si un fichier correspond, tous les fichiers de la publication sont téléchargés. Si aucune correspondance de fichier, il vérifie alors les commentaires de la publication. Si un commentaire correspond, tous les fichiers sont téléchargés. (Utilise plus de requêtes API). Le nommage du dossier priorise la correspondance de fichier, puis la correspondance de commentaire.</li>\n</ul>\n</li>\n<li><b>🗄️ Nom de dossier personnalisé (Publication unique uniquement) :</b>\n<ul>\n<li>Visible et utilisable uniquement lors du téléchargement d'une URL de publication spécifique ET si 'Dossiers séparés par Nom/Titre' est activé.</li>\n<li>Permet de spécifier un nom personnalisé pour le dossier de téléchargement de cette seule publication.</li>\n</ul>\n</li>\n<li><b>🚫 Ignorer avec les mots :</b>\n<ul><li>Saisissez des mots, séparés par des virgules (par ex., <code>WIP, sketch, preview</code>) pour ignorer certains contenus.</li></ul>\n</li>\n<li><b>Portée : Bouton [Type] (Portée des mots à ignorer) :</b> Cycle la façon dont 'Ignorer avec les mots' s'applique :\n<ul>\n<li><code>Portée : Fichiers</code> : Ignore les fichiers individuels si leurs noms contiennent l'un de ces mots.</li>\n<li><code>Portée : Publications</code> : Ignore les publications entières si leurs titres contiennent l'un de ces mots.</li>\n<li><code>Portée : Les deux</code> : Applique les deux (titre de la publication d'abord, puis fichiers individuels).</li>\n</ul>\n</li>\n<li><b>✂️ Supprimer les mots du nom :</b>\n<ul><li>Saisissez des mots, séparés par des virgules (par ex., <code>patreon, [HD]</code>), à supprimer des noms de fichiers téléchargés (insensible à la casse).</li></ul>\n</li>\n<li><b>Filtrer les fichiers (Boutons radio) :</b> Choisissez ce qu'il faut télécharger :\n<ul>\n<li><code>Tout</code> : Télécharge tous les types de fichiers trouvés.</li>\n<li><code>Images/GIFs</code> : Uniquement les formats d'image courants (JPG, PNG, GIF, WEBP, etc.) et les GIFs.</li>\n<li><code>Vidéos</code> : Uniquement les formats vidéo courants (MP4, MKV, WEBM, MOV, etc.).</li>\n<li><code>📦 Archives Uniquement</code> : Télécharge exclusivement les fichiers <b>.zip</b> et <b>.rar</b>. Lorsque cette option est sélectionnée, les cases à cocher 'Ignorer .zip' et 'Ignorer .rar' sont automatiquement désactivées et décochées. 'Afficher les liens externes' est également désactivé.</li>\n<li><code>🎧 Audio Uniquement</code> : Télécharge uniquement les formats audio courants (MP3, WAV, FLAC, M4A, OGG, etc.). Les autres options spécifiques aux fichiers se comportent comme en mode 'Images' ou 'Vidéos'.</li>\n<li><code>🔗 Liens Uniquement</code> : Extrait et affiche les liens externes des descriptions de publications au lieu de télécharger des fichiers. Les options liées au téléchargement et 'Afficher les liens externes' sont désactivées. Le bouton de téléchargement principal devient '🔗 Extraire les liens'.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step3_title":"③ Options de téléchargement & Paramètres",
"help_guide_step3_content":"<html><head/><body>\n<h3>Options de téléchargement & Paramètres (Panneau de gauche)</h3>\n<ul>\n<li><b>Ignorer .zip / Ignorer .rar :</b> Cases à cocher pour éviter de télécharger ces types de fichiers d'archive. (Désactivées et ignorées si le mode de filtre '📦 Archives Uniquement' est sélectionné).</li>\n<li><b>Télécharger les miniatures uniquement :</b> Télécharge les petites images d'aperçu au lieu des fichiers en taille réelle (si disponible).</li>\n<li><b>Compresser les grandes images (en WebP) :</b> Si la bibliothèque 'Pillow' (PIL) est installée, les images de plus de 1.5 Mo seront converties au format WebP si la version WebP est significativement plus petite.</li>\n<li><b>⚙️ Paramètres avancés :</b>\n<ul>\n<li><b>Dossiers séparés par Nom/Titre :</b> Crée des sous-dossiers basés sur l'entrée 'Filtrer par Personnage(s)' ou les titres des publications. Peut utiliser la liste <b>Known.txt</b> comme solution de repli pour les noms de dossiers.</li></ul></li></ul></body></html>",
"help_guide_step4_title":"④ Paramètres avancés (Partie 1)",
"help_guide_step4_content":"<html><head/><body><h3>⚙️ Paramètres avancés (Suite)</h3><ul><ul>\n<li><b>Sous-dossier par publication :</b> Si 'Dossiers séparés' est activé, cela crée un sous-dossier supplémentaire pour <i>chaque publication individuelle</i> à l'intérieur du dossier principal personnage/titre.</li>\n<li><b>Utiliser le cookie :</b> Cochez cette case pour utiliser des cookies pour les requêtes.\n<ul>\n<li><b>Champ de texte :</b> Saisissez une chaîne de cookie directement (par ex., <code>nom1=valeur1; nom2=valeur2</code>).</li>\n<li><b>Parcourir... :</b> Sélectionnez un fichier <code>cookies.txt</code> (format Netscape). Le chemin apparaîtra dans le champ de texte.</li>\n<li><b>Priorité :</b> Le champ de texte (s'il est rempli) a la priorité sur un fichier parcouru. Si 'Utiliser le cookie' est coché mais que les deux sont vides, il tente de charger <code>cookies.txt</code> depuis le répertoire de l'application.</li>\n</ul>\n</li>\n<li><b>Utiliser le multithreading & Entrée Threads :</b>\n<ul>\n<li>Active des opérations plus rapides. Le nombre dans l'entrée 'Threads' signifie :\n<ul>\n<li>Pour les <b>Flux de créateurs :</b> Nombre de publications à traiter simultanément. Les fichiers de chaque publication sont téléchargés séquentiellement par son worker (sauf si le nommage de manga 'Basé sur la date' est activé, ce qui force 1 worker de publication).</li>\n<li>Pour les <b>URL de publications uniques :</b> Nombre de fichiers à télécharger simultanément à partir de cette seule publication.</li>\n</ul>\n</li>\n<li>Si décoché, 1 thread est utilisé. Des nombres élevés de threads (par ex., >40) peuvent afficher un avertissement.</li>\n</ul>\n</li></ul></ul></body></html>",
"help_guide_step5_title":"⑤ Paramètres avancés (Partie 2) & Actions",
"help_guide_step5_content":"<html><head/><body><h3>⚙️ Paramètres avancés (Suite)</h3><ul><ul>\n<li><b>Afficher les liens externes dans le journal :</b> Si coché, un panneau de journal secondaire apparaît sous le journal principal pour afficher les liens externes trouvés dans les descriptions de publications. (Désactivé si le mode '🔗 Liens Uniquement' ou '📦 Archives Uniquement' est actif).</li>\n<li><b>📖 Mode Manga/BD (URL de créateur uniquement) :</b> Conçu pour le contenu séquentiel.\n<ul>\n<li>Télécharge les publications du <b>plus ancien au plus récent</b>.</li>\n<li>L'entrée 'Plage de pages' est désactivée car toutes les publications sont récupérées.</li>\n<li>Un <b>bouton de bascule de style de nom de fichier</b> (par ex., 'Nom : Titre de la publication') apparaît en haut à droite de la zone du journal lorsque ce mode est actif pour un flux de créateur. Cliquez dessus pour cycler entre les styles de nommage :\n<ul>\n<li><code>Nom : Titre de la publication (Défaut)</code> : Le premier fichier d'une publication est nommé d'après le titre nettoyé de la publication (par ex., 'Mon Chapitre 1.jpg'). Les fichiers suivants dans la *même publication* tenteront de conserver leurs noms de fichiers originaux (par ex., 'page_02.png', 'bonus_art.jpg'). Si la publication n'a qu'un seul fichier, il est nommé d'après le titre de la publication. C'est généralement recommandé pour la plupart des mangas/BD.</li>\n<li><code>Nom : Fichier original</code> : Tous les fichiers tentent de conserver leurs noms de fichiers originaux.</li>\n<li><code>Nom : Fichier original</code> : Tous les fichiers tentent de conserver leurs noms de fichiers originaux. Lorsque ce style est actif, un champ de saisie pour un <b>préfixe de nom de fichier optionnel</b> (par ex., 'MaSerie_') apparaîtra à côté de ce bouton de style. Exemple : 'MaSerie_FichierOriginal.jpg'.</li>\n<li><code>Nom : Titre+Num.G (Titre de la publication + Numérotation globale)</code> : Tous les fichiers de toutes les publications de la session de téléchargement actuelle sont nommés séquentiellement en utilisant le titre nettoyé de la publication comme préfixe, suivi d'un compteur global. Exemple : Publication 'Chapitre 1' (2 fichiers) -> 'Chapitre 1 001.jpg', 'Chapitre 1 002.png'. Publication suivante 'Chapitre 2' (1 fichier) -> 'Chapitre 2 003.jpg'. Le multithreading pour le traitement des publications est automatiquement désactivé pour ce style.</li>\n<li><code>Nom : Basé sur la date</code> : Les fichiers sont nommés séquentiellement (001.ext, 002.ext, ...) en fonction de l'ordre de publication. Lorsque ce style est actif, un champ de saisie pour un <b>préfixe de nom de fichier optionnel</b> (par ex., 'MaSerie_') apparaîtra à côté de ce bouton de style. Exemple : 'MaSerie_001.jpg'. Le multithreading pour le traitement des publications est automatiquement désactivé pour ce style.</li>\n</ul>\n</li>\n<li>Pour de meilleurs résultats avec les styles 'Nom : Titre de la publication', 'Nom : Titre+Num.G' ou 'Nom : Basé sur la date', utilisez le champ 'Filtrer par Personnage(s)' avec le titre du manga/de la série pour l'organisation des dossiers.</li>\n</ul>\n</li>\n</ul></li></ul>\n<h3>Actions principales (Panneau de gauche)</h3>\n<ul>\n<li><b>⬇️ Démarrer le téléchargement / 🔗 Extraire les liens :</b> Le texte et la fonction de ce bouton changent en fonction de la sélection du bouton radio 'Filtrer les fichiers'. Il démarre l'opération principale.</li>\n<li><b>⏸️ Mettre en pause le téléchargement / ▶️ Reprendre le téléchargement :</b> Permet d'arrêter temporairement le processus de téléchargement/extraction en cours et de le reprendre plus tard. Certains paramètres de l'UI peuvent être modifiés pendant la pause.</li>\n<li><b>❌ Annuler & Réinitialiser l'UI :</b> Arrête l'opération en cours et effectue une réinitialisation logicielle de l'UI. Vos entrées d'URL et de répertoire de téléchargement sont conservées, mais les autres paramètres et journaux sont effacés.</li>\n</ul></body></html>",
"help_guide_step6_title":"⑥ Liste des séries/personnages connus",
"help_guide_step6_content":"<html><head/><body>\n<h3>Gestion de la liste des séries/personnages connus (en bas à gauche)</h3>\n<p>Cette section aide à gérer le fichier <code>Known.txt</code>, qui est utilisé pour l'organisation intelligente des dossiers lorsque 'Dossiers séparés par Nom/Titre' est activé, en particulier comme solution de repli si une publication ne correspond pas à votre entrée active 'Filtrer par Personnage(s)'.</p>\n<ul>\n<li><b>Ouvrir Known.txt :</b> Ouvre le fichier <code>Known.txt</code> (situé dans le répertoire de l'application) dans votre éditeur de texte par défaut pour une édition avancée (comme la création d'alias groupés complexes).</li>\n<li><b>Rechercher des personnages... :</b> Filtre la liste des noms connus affichée ci-dessous.</li>\n<li><b>Widget de liste :</b> Affiche les noms principaux de votre <code>Known.txt</code>. Sélectionnez des entrées ici pour les supprimer.</li>\n<li><b>Ajouter un nouveau nom de série/personnage (Champ de saisie) :</b> Saisissez un nom ou un groupe à ajouter.\n<ul>\n<li><b>Nom simple :</b> par ex., <code>Ma Super Série</code>. Ajoute comme une seule entrée.</li>\n<li><b>Groupe pour des entrées Known.txt séparées :</b> par ex., <code>(Vivi, Ulti, Uta)</code>. Ajoute \"Vivi\", \"Ulti\" et \"Uta\" comme trois entrées individuelles séparées à <code>Known.txt</code>.</li>\n<li><b>Groupe pour dossier partagé & Entrée Known.txt unique (Tilde <code>~</code>) :</b> par ex., <code>(Personnage A, Perso A)~</code>. Ajoute une entrée à <code>Known.txt</code> nommée \"Personnage A Perso A\". \"Personnage A\" et \"Perso A\" deviennent des alias pour ce seul dossier/entrée.</li>\n</ul>\n</li>\n<li><b>Bouton ➕ Ajouter :</b> Ajoute le nom/groupe du champ de saisie ci-dessus à la liste et à <code>Known.txt</code>.</li>\n<li><b>Bouton ⤵️ Ajouter au filtre :</b>\n<ul>\n<li>Situé à côté du bouton '➕ Ajouter' pour la liste 'Séries/Personnages connus'.</li>\n<li>Cliquer sur ce bouton ouvre une fenêtre popup affichant tous les noms de votre fichier <code>Known.txt</code>, chacun avec une case à cocher.</li>\n<li>La popup inclut une barre de recherche pour filtrer rapidement la liste des noms.</li>\n<li>Vous pouvez sélectionner un ou plusieurs noms en utilisant les cases à cocher.</li>\n<li>Cliquez sur 'Ajouter la sélection' pour insérer les noms choisis dans le champ de saisie 'Filtrer par Personnage(s)' de la fenêtre principale.</li>\n<li>Si un nom sélectionné dans <code>Known.txt</code> était à l'origine un groupe (par ex., défini comme <code>(Boa, Hancock)</code> dans Known.txt), il sera ajouté au champ de filtre comme <code>(Boa, Hancock)~</code>. Les noms simples sont ajoutés tels quels.</li>\n<li>Les boutons 'Tout sélectionner' et 'Tout désélectionner' sont disponibles dans la popup pour plus de commodité.</li>\n<li>Cliquez sur 'Annuler' pour fermer la popup sans aucune modification.</li>\n</ul>\n</li>\n<li><b>Bouton 🗑️ Supprimer la sélection :</b> Supprime le(s) nom(s) sélectionné(s) de la liste et de <code>Known.txt</code>.</li>\n<li><b>Bouton ❓ (Celui-ci !) :</b> Affiche ce guide d'aide complet.</li>\n</ul></body></html>",
"help_guide_step7_title":"⑦ Zone de journal & Contrôles",
"help_guide_step7_content":"<html><head/><body>\n<h3>Zone de journal & Contrôles (Panneau de droite)</h3>\n<ul>\n<li><b>📜 Journal de progression / Journal des liens extraits (Étiquette) :</b> Titre de la zone de journal principale ; change si le mode '🔗 Liens Uniquement' est actif.</li>\n<li><b>Rechercher des liens... / Bouton 🔍 (Recherche de liens) :</b>\n<ul><li>Visible uniquement lorsque le mode '🔗 Liens Uniquement' est actif. Permet de filtrer en temps réel les liens extraits affichés dans le journal principal par texte, URL ou plateforme.</li></ul>\n</li>\n<li><b>Nom : Bouton [Style] (Style de nom de fichier Manga) :</b>\n<ul><li>Visible uniquement lorsque le <b>Mode Manga/BD</b> est actif pour un flux de créateur et non en mode 'Liens Uniquement' ou 'Archives Uniquement'.</li>\n<li>Cycle entre les styles de nom de fichier : <code>Titre de la publication</code>, <code>Fichier original</code>, <code>Basé sur la date</code>. (Voir la section Mode Manga/BD pour plus de détails).</li>\n<li>Lorsque le style 'Fichier original' ou 'Basé sur la date' est actif, un champ de saisie pour un <b>préfixe de nom de fichier optionnel</b> apparaîtra à côté de ce bouton.</li>\n</ul>\n</li>\n<li><b>Bouton Multi-partie : [ON/OFF] :</b>\n<ul><li>Bascule les téléchargements multi-segments pour les fichiers volumineux individuels.\n<ul><li><b>ON :</b> Peut accélérer les téléchargements de fichiers volumineux (par ex., des vidéos) mais peut augmenter les saccades de l'UI ou le spam du journal avec de nombreux petits fichiers. Un avertissement apparaît lors de l'activation. Si un téléchargement multi-partie échoue, il réessaie en flux unique.</li>\n<li><b>OFF (Défaut) :</b> Les fichiers sont téléchargés en un seul flux.</li>\n</ul>\n<li>Désactivé si le mode '🔗 Liens Uniquement' ou '📦 Archives Uniquement' est actif.</li>\n</ul>\n</li>\n<li><b>Bouton 👁️ / 🙈 (Bascule d'affichage du journal) :</b> Change la vue du journal principal :\n<ul>\n<li><b>👁️ Journal de progression (Défaut) :</b> Affiche toute l'activité de téléchargement, les erreurs et les résumés.</li>\n<li><b>🙈 Journal des personnages manqués :</b> Affiche une liste de termes clés des titres/contenus de publications qui ont été ignorés en raison de vos paramètres 'Filtrer par Personnage(s)'. Utile pour identifier le contenu que vous pourriez manquer involontairement.</li>\n</ul>\n</li>\n<li><b>Bouton 🔄 Réinitialiser :</b> Efface tous les champs de saisie, les journaux et réinitialise les paramètres temporaires à leurs valeurs par défaut. Ne peut être utilisé que lorsqu'aucun téléchargement n'est actif.</li>\n<li><b>Sortie du journal principal (Zone de texte) :</b> Affiche les messages de progression détaillés, les erreurs et les résumés. Si le mode '🔗 Liens Uniquement' est actif, cette zone affiche les liens extraits.</li>\n<li><b>Sortie du journal des personnages manqués (Zone de texte) :</b> (Visible via la bascule 👁️ / 🙈) Affiche les publications/fichiers ignorés en raison des filtres de personnages.</li>\n<li><b>Sortie du journal externe (Zone de texte) :</b> Apparaît sous le journal principal si 'Afficher les liens externes dans le journal' est coché. Affiche les liens externes trouvés dans les descriptions de publications.</li>\n<li><b>Bouton Exporter les liens :</b>\n<ul><li>Visible et activé uniquement lorsque le mode '🔗 Liens Uniquement' est actif et que des liens ont été extraits.</li>\n<li>Permet d'enregistrer tous les liens extraits dans un fichier <code>.txt</code>.</li>\n</ul>\n</li>\n<li><b>Étiquette de progression : [Statut] :</b> Affiche la progression globale du processus de téléchargement ou d'extraction de liens (par ex., publications traitées).</li>\n<li><b>Étiquette de progression des fichiers :</b> Affiche la progression des téléchargements de fichiers individuels, y compris la vitesse et la taille, ou l'état du téléchargement multi-partie.</li>\n</ul></body></html>",
"help_guide_step8_title":"⑧ Mode Favori & Fonctionnalités futures",
"help_guide_step8_content":"<html><head/><body>\n<h3>Mode Favori (Téléchargement depuis vos favoris Kemono.su)</h3>\n<p>Ce mode vous permet de télécharger du contenu directement depuis les artistes que vous avez mis en favoris sur Kemono.su.</p>\n<ul>\n<li><b>⭐ Comment l'activer :</b>\n<ul>\n<li>Cochez la case <b>'⭐ Mode Favori'</b>, située à côté du bouton radio '🔗 Liens Uniquement'.</li>\n</ul>\n</li>\n<li><b>Changements de l'UI en Mode Favori :</b>\n<ul>\n<li>La zone de saisie '🔗 URL Créateur/Post Kemono' est remplacée par un message indiquant que le Mode Favori est actif.</li>\n<li>Les boutons standard 'Démarrer le téléchargement', 'Pause', 'Annuler' sont remplacés par :\n<ul>\n<li>Bouton <b>'🖼️ Artistes favoris'</b></li>\n<li>Bouton <b>'📄 Publications favorites'</b></li>\n</ul>\n</li>\n<li>L'option '🍪 Utiliser le cookie' est automatiquement activée et verrouillée, car les cookies sont nécessaires pour récupérer vos favoris.</li>\n</ul>\n</li>\n<li><b>Bouton 🖼️ Artistes favoris :</b>\n<ul>\n<li>Cliquer ici ouvre une boîte de dialogue qui liste tous les artistes que vous avez mis en favoris sur Kemono.su.</li>\n<li>Vous pouvez sélectionner un ou plusieurs artistes de cette liste pour télécharger leur contenu.</li>\n</ul>\n</li>\n<li><b>Bouton 📄 Publications favorites (Fonctionnalité future) :</b>\n<ul>\n<li>Le téléchargement de <i>publications</i> spécifiques mises en favoris (en particulier dans un ordre séquentiel de type manga si elles font partie d'une série) est une fonctionnalité actuellement en développement.</li>\n<li>La meilleure façon de gérer les publications favorites, en particulier pour une lecture séquentielle comme les mangas, est encore à l'étude.</li>\n<li>Si vous avez des idées spécifiques ou des cas d'utilisation sur la façon dont vous aimeriez télécharger et organiser les publications favorites (par ex., \"style manga\" à partir des favoris), veuillez envisager d'ouvrir une issue ou de rejoindre la discussion sur la page GitHub du projet. Votre contribution est précieuse !</li>\n</ul>\n</li>\n<li><b>Portée de téléchargement des favoris (Bouton) :</b>\n<ul>\n<li>Ce bouton (à côté de 'Publications favorites') contrôle où le contenu des artistes favoris sélectionnés est téléchargé :\n<ul>\n<li><b><i>Portée : Emplacement sélectionné :</i></b> Tous les artistes sélectionnés sont téléchargés dans l' 'Emplacement de téléchargement' principal que vous avez défini dans l'UI. Les filtres s'appliquent globalement à tout le contenu.</li>\n<li><b><i>Portée : Dossiers d'artistes :</i></b> Pour chaque artiste sélectionné, un sous-dossier (nommé d'après l'artiste) est automatiquement créé à l'intérieur de votre 'Emplacement de téléchargement' principal. Le contenu de cet artiste va dans son dossier spécifique. Les filtres s'appliquent à l'intérieur du dossier dédié de chaque artiste.</li>\n</ul>\n</li>\n</ul>\n</li>\n<li><b>Filtres en Mode Favori :</b>\n<ul>\n<li>Les options '🎯 Filtrer par Personnage(s)', '🚫 Ignorer avec les mots' et 'Filtrer les fichiers' que vous avez définies dans l'UI s'appliqueront toujours au contenu téléchargé de vos artistes favoris sélectionnés.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step9_title":"⑨ Fichiers clés & Visite",
"help_guide_step9_content":"<html><head/><body>\n<h3>Fichiers clés utilisés par l'application</h3>\n<ul>\n<li><b><code>Known.txt</code> :</b>\n<ul>\n<li>Situé dans le répertoire de l'application (où se trouve le <code>.exe</code> ou <code>main.py</code>).</li>\n<li>Stocke votre liste de séries, personnages ou titres de séries connus pour l'organisation automatique des dossiers lorsque 'Dossiers séparés par Nom/Titre' est activé.</li>\n<li><b>Format :</b>\n<ul>\n<li>Chaque ligne est une entrée.</li>\n<li><b>Nom simple :</b> par ex., <code>Ma Super Série</code>. Le contenu correspondant ira dans un dossier nommé \"Ma Super Série\".</li>\n<li><b>Alias groupés :</b> par ex., <code>(Personnage A, Perso A, Nom Alt A)</code>. Le contenu correspondant à \"Personnage A\", \"Perso A\", OU \"Nom Alt A\" ira TOUS dans un seul dossier nommé \"Personnage A Perso A Nom Alt A\" (après nettoyage). Tous les termes entre parenthèses deviennent des alias pour ce dossier.</li>\n</ul>\n</li>\n<li><b>Utilisation :</b> Sert de solution de repli pour le nommage des dossiers si une publication ne correspond pas à votre entrée active 'Filtrer par Personnage(s)'. Vous pouvez gérer les entrées simples via l'UI ou éditer le fichier directement pour les alias complexes. L'application le recharge au démarrage ou à la prochaine utilisation.</li>\n</ul>\n</li>\n<li><b><code>cookies.txt</code> (Optionnel) :</b>\n<ul>\n<li>Si vous utilisez la fonctionnalité 'Utiliser le cookie' et que vous ne fournissez pas de chaîne de cookie directe ou que vous ne parcourez pas un fichier spécifique, l'application cherchera un fichier nommé <code>cookies.txt</code> dans son répertoire.</li>\n<li><b>Format :</b> Doit être au format de fichier de cookie Netscape.</li>\n<li><b>Utilisation :</b> Permet au téléchargeur d'utiliser la session de connexion de votre navigateur pour accéder au contenu qui pourrait être derrière une connexion sur Kemono/Coomer.</li>\n</ul>\n</li>\n</ul>\n<h3>Visite pour le premier utilisateur</h3>\n<ul>\n<li>Au premier lancement (ou si réinitialisé), une boîte de dialogue de visite de bienvenue apparaît, vous guidant à travers les principales fonctionnalités. Vous pouvez la passer ou choisir de \"Ne plus jamais afficher cette visite.\"</li>\n</ul>\n<p><em>De nombreux éléments de l'UI ont également des info-bulles qui apparaissent lorsque vous survolez votre souris, fournissant des conseils rapides.</em></p>\n</body></html>"
}

translations ["en"].update ({
"help_guide_dialog_title":"Kemono Downloader - Feature Guide",
"help_guide_github_tooltip":"Visit project's GitHub page (Opens in browser)",
"help_guide_instagram_tooltip":"Visit our Instagram page (Opens in browser)",
"help_guide_discord_tooltip":"Visit our Discord community (Opens in browser)",
"help_guide_step1_title":"① Introduction & Main Inputs",
"help_guide_step1_content":"""<html><head/><body>
    <p>This guide provides an overview of the Kemono Downloader's features, fields, and buttons.</p>
    <h3>Main Input Area (Top Left)</h3>
    <ul>
        <li><b>🔗 Kemono Creator/Post URL:</b>
            <ul>
                <li>Enter the full web address of a creator's page (e.g., <i>https://kemono.su/patreon/user/12345</i>) or a specific post (e.g., <i>.../post/98765</i>).</li>
                <li>Supports Kemono (kemono.su, kemono.party) and Coomer (coomer.su, coomer.party) URLs.</li>
            </ul>
        </li>
        <li><b>Page Range (Start to End):</b>
            <ul>
                <li>For creator URLs: Specify a range of pages to fetch (e.g., pages 2 to 5). Leave blank for all pages.</li>
                <li>Disabled for single post URLs or when <b>Manga/Comic Mode</b> is active.</li>
            </ul>
        </li>
        <li><b>📁 Download Location:</b>
            <ul>
                <li>Click <b>'Browse...'</b> to choose a main folder on your computer where all downloaded files will be saved.</li>
                <li>This field is required unless you are using <b>'🔗 Only Links'</b> mode.</li>
            </ul>
        </li>
        <li><b>🎨 Creator Selection Button (Next to URL Input):</b>
            <ul>
                <li>Click the palette icon (🎨) to open the 'Creator Selection' dialog.</li>
                <li>This dialog loads creators from your <code>creators.json</code> file (which should be in the application's directory).</li>
                <li><b>Inside the Dialog:</b>
                    <ul>
                        <li><b>Search Bar:</b> Type to filter the list of creators by name or service.</li>
                        <li><b>Creator List:</b> Displays creators from your <code>creators.json</code>. Creators you have 'favorited' (in the JSON data) appear at the top.</li>
                        <li><b>Checkboxes:</b> Select one or more creators by checking the box next to their name.</li>
                        <li><b>'Scope' Button (e.g., 'Scope: Characters'):</b> This button toggles the download organization when initiating downloads from this popup:
                            <ul><li><i>Scope: Characters:</i> Downloads will be organized into character-named folders directly within your main 'Download Location'. Art from different creators for the same character will be grouped together.</li>
                                <li><i>Scope: Creators:</i> Downloads will first create a folder named after the creator within your main 'Download Location'. Character-named subfolders will then be created inside each creator's folder.</li></ul>
                        </li>
                        <li><b>'Add Selected' Button:</b> Clicking this will take the names of all checked creators and add them to the main '🔗 Kemono Creator/Post URL' input field, separated by commas. The dialog will then close.</li>
                    </ul>
                </li>
                <li>This feature provides a quick way to populate the URL field for multiple creators without manually typing or pasting each URL.</li>
            </ul>
        </li>
    </ul></body></html>""",
"help_guide_step2_title":"② Filtering Downloads",
"help_guide_step2_content":"""<html><head/><body>
    <h3>Filtering Downloads (Left Panel)</h3>
    <ul>
        <li><b>🎯 Filter by Character(s):</b>
            <ul>
                <li>Enter names, comma-separated (e.g., <code>Tifa, Aerith</code>).</li>
                <li><b>Grouped Aliases for Shared Folder (Separate Known.txt Entries):</b> <code>(Vivi, Ulti, Uta)</code>.
                    <ul><li>Content matching "Vivi", "Ulti", OR "Uta" will go into a shared folder named "Vivi Ulti Uta" (after cleaning).</li>
                        <li>If these names are new, "Vivi", "Ulti", and "Uta" will be prompted to be added as <i>separate individual entries</i> to <code>Known.txt</code>.</li>
                    </ul>
                </li>
                <li><b>Grouped Aliases for Shared Folder (Single Known.txt Entry):</b> <code>(Yuffie, Sonon)~</code> (note the tilde <code>~</code>).
                    <ul><li>Content matching "Yuffie" OR "Sonon" will go into a shared folder named "Yuffie Sonon".</li>
                        <li>If new, "Yuffie Sonon" (with aliases Yuffie, Sonon) will be prompted to be added as a <i>single group entry</i> to <code>Known.txt</code>.</li>
                    </ul>
                </li>
                <li>This filter influences folder naming if 'Separate Folders by Name/Title' is enabled.</li>
            </ul>
        </li>
        <li><b>Filter: [Type] Button (Character Filter Scope):</b> Cycles how the 'Filter by Character(s)' applies:
            <ul>
                <li><code>Filter: Files</code>: Checks individual filenames. A post is kept if any file matches; only matching files are downloaded. Folder naming uses the character from the matching filename.</li>
                <li><code>Filter: Title</code>: Checks post titles. All files from a matching post are downloaded. Folder naming uses the character from the matching post title.</li>
                <li><code>Filter: Both</code>: Checks post title first. If it matches, all files are downloaded. If not, it then checks filenames, and only matching files are downloaded. Folder naming prioritizes title match, then file match.</li>
                <li><code>Filter: Comments (Beta)</code>: Checks filenames first. If a file matches, all files from the post are downloaded. If no file match, it then checks post comments. If a comment matches, all files are downloaded. (Uses more API requests). Folder naming prioritizes file match, then comment match.</li>
            </ul>
        </li>
        <li><b>🗄️ Custom Folder Name (Single Post Only):</b>
            <ul>
                <li>Visible and usable only when downloading a single specific post URL AND 'Separate Folders by Name/Title' is enabled.</li>
                <li>Allows you to specify a custom name for that single post's download folder.</li>
            </ul>
        </li>
        <li><b>🚫 Skip with Words:</b>
            <ul><li>Enter words, comma-separated (e.g., <code>WIP, sketch, preview</code>) to skip certain content.</li></ul>
        </li>
        <li><b>Scope: [Type] Button (Skip Words Scope):</b> Cycles how 'Skip with Words' applies:
            <ul>
                <li><code>Scope: Files</code>: Skips individual files if their names contain any of these words.</li>
                <li><code>Scope: Posts</code>: Skips entire posts if their titles contain any of these words.</li>
                <li><code>Scope: Both</code>: Applies both (post title first, then individual files).</li>
            </ul>
        </li>
        <li><b>✂️ Remove Words from name:</b>
            <ul><li>Enter words, comma-separated (e.g., <code>patreon, [HD]</code>), to remove from downloaded filenames (case-insensitive).</li></ul>
        </li>
        <li><b>Filter Files (Radio Buttons):</b> Choose what to download:
            <ul>
                <li><code>All</code>: Downloads all file types found.</li>
                <li><code>Images/GIFs</code>: Only common image formats (JPG, PNG, GIF, WEBP, etc.) and GIFs.</li>
                <li><code>Videos</code>: Only common video formats (MP4, MKV, WEBM, MOV, etc.).</li>
                <li><code>📦 Only Archives</code>: Exclusively downloads <b>.zip</b> and <b>.rar</b> files. When selected, 'Skip .zip' and 'Skip .rar' checkboxes are automatically disabled and unchecked. 'Show External Links' is also disabled.</li>
                <li><code>🎧 Only Audio</code>: Downloads only common audio formats (MP3, WAV, FLAC, M4A, OGG, etc.). Other file-specific options behave as with 'Images' or 'Videos' mode.</li>
                <li><code>🔗 Only Links</code>: Extracts and displays external links from post descriptions instead of downloading files. Download-related options and 'Show External Links' are disabled. The main download button changes to '🔗 Extract Links'.</li>                    
            </ul>
        </li>
    </ul></body></html>""",
"help_guide_step3_title":"③ Download Options & Settings",
"help_guide_step3_content":"""<html><head/><body>
    <h3>Download Options & Settings (Left Panel)</h3>
    <ul>
        <li><b>Skip .zip / Skip .rar:</b> Checkboxes to avoid downloading these archive file types. (Disabled and ignored if '📦 Only Archives' filter mode is selected).</li>
        <li><b>Download Thumbnails Only:</b> Downloads small preview images instead of full-sized files (if available).</li>
        <li><b>Compress Large Images (to WebP):</b> If the 'Pillow' (PIL) library is installed, images larger than 1.5MB will be converted to WebP format if the WebP version is significantly smaller.</li>
        <li><b>⚙️ Advanced Settings:</b>
            <ul>
                <li><b>Separate Folders by Name/Title:</b> Creates subfolders based on the 'Filter by Character(s)' input or post titles. Can use the <b>Known.txt</b> list as a fallback for folder names.</li></ul></li></ul></body></html>""",
"help_guide_step4_title":"④ Advanced Settings (Part 1)",
"help_guide_step4_content":"""<html><head/><body><h3>⚙️ Advanced Settings (Continued)</h3><ul><ul>
                <li><b>Subfolder per Post:</b> If 'Separate Folders' is on, this creates an additional subfolder for <i>each individual post</i> inside the main character/title folder.</li>
                <li><b>Use Cookie:</b> Check this to use cookies for requests.
                    <ul>
                        <li><b>Text Field:</b> Enter a cookie string directly (e.g., <code>name1=value1; name2=value2</code>).</li>
                        <li><b>Browse...:</b> Select a <code>cookies.txt</code> file (Netscape format). The path will appear in the text field.</li>
                        <li><b>Precedence:</b> The text field (if filled) takes precedence over a browsed file. If 'Use Cookie' is checked but both are empty, it attempts to load <code>cookies.txt</code> from the app's directory.</li>
                    </ul>
                </li>
                <li><b>Use Multithreading & Threads Input:</b>
                    <ul>
                        <li>Enables faster operations. The number in 'Threads' input means:
                            <ul>
                                <li>For <b>Creator Feeds:</b> Number of posts to process simultaneously. Files within each post are downloaded sequentially by its worker (unless 'Date Based' manga naming is on, which forces 1 post worker).</li>
                                <li>For <b>Single Post URLs:</b> Number of files to download concurrently from that single post.</li>
                            </ul>
                        </li>
                        <li>If unchecked, 1 thread is used. High thread counts (e.g., >40) may show an advisory.</li>
                    </ul>
                </li></ul></ul></body></html>""",
"help_guide_step5_title":"⑤ Advanced Settings (Part 2) & Actions",
"help_guide_step5_content":"""<html><head/><body><h3>⚙️ Advanced Settings (Continued)</h3><ul><ul>
                <li><b>Show External Links in Log:</b> If checked, a secondary log panel appears below the main log to display any external links found in post descriptions. (Disabled if '🔗 Only Links' or '📦 Only Archives' mode is active).</li>
                <li><b>📖 Manga/Comic Mode (Creator URLs only):</b> Tailored for sequential content.
                    <ul>
                        <li>Downloads posts from <b>oldest to newest</b>.</li>
                        <li>The 'Page Range' input is disabled as all posts are fetched.</li>
                        <li>A <b>filename style toggle button</b> (e.g., 'Name: Post Title') appears in the top-right of the log area when this mode is active for a creator feed. Click it to cycle through naming styles:
                            <ul>
                                <li><code>Name: Post Title (Default)</code>: The first file in a post is named after the post's cleaned title (e.g., 'My Chapter 1.jpg'). Subsequent files within the *same post* will attempt to keep their original filenames (e.g., 'page_02.png', 'bonus_art.jpg'). If the post has only one file, it's named after the post title. This is generally recommended for most manga/comics.</li>
                                <li><code>Name: Original File</code>: All files attempt to keep their original filenames.</li>
                                <li><code>Name: Original File</code>: All files attempt to keep their original filenames. When this style is active, an input field for an <b>optional filename prefix</b> (e.g., 'MySeries_') will appear next to this style button. Example: 'MySeries_OriginalFile.jpg'.</li>
                                <li><code>Name: Title+G.Num (Post Title + Global Numbering)</code>: All files across all posts in the current download session are named sequentially using the post's cleaned title as a prefix, followed by a global counter. Example: Post 'Chapter 1' (2 files) -> 'Chapter 1 001.jpg', 'Chapter 1 002.png'. Next post 'Chapter 2' (1 file) -> 'Chapter 2 003.jpg'. Multithreading for post processing is automatically disabled for this style.</li>
                                <li><code>Name: Date Based</code>: Files are named sequentially (001.ext, 002.ext, ...) based on post publication order. When this style is active, an input field for an <b>optional filename prefix</b> (e.g., 'MySeries_') will appear next to this style button. Example: 'MySeries_001.jpg'. Multithreading for post processing is automatically disabled for this style.</li>
                            </ul>
                        </li>
                        <li>For best results with 'Name: Post Title', 'Name: Title+G.Num', or 'Name: Date Based' styles, use the 'Filter by Character(s)' field with the manga/series title for folder organization.</li>
                    </ul>
                </li>
            </ul></li></ul>
    
    <h3>Main Action Buttons (Left Panel)</h3>
    <ul>
        <li><b>⬇️ Start Download / 🔗 Extract Links:</b> This button's text and function change based on the 'Filter Files' radio button selection. It starts the primary operation.</li>
        <li><b>⏸️ Pause Download / ▶️ Resume Download:</b> Allows you to temporarily halt the current download/extraction process and resume it later. Some UI settings can be changed while paused.</li>
        <li><b>❌ Cancel & Reset UI:</b> Stops the current operation and performs a soft UI reset. Your URL and Download Directory inputs are preserved, but other settings and logs are cleared.</li>
    </ul></body></html>""",
"help_guide_step6_title":"⑥ Known Shows/Characters List",
"help_guide_step6_content":"""<html><head/><body>
    <h3>Known Shows/Characters List Management (Bottom Left)</h3>
    <p>This section helps manage the <code>Known.txt</code> file, which is used for smart folder organization when 'Separate Folders by Name/Title' is enabled, especially as a fallback if a post doesn't match your active 'Filter by Character(s)' input.</p>
    <ul>
        <li><b>Open Known.txt:</b> Opens the <code>Known.txt</code> file (located in the app's directory) in your default text editor for advanced editing (like creating complex grouped aliases).</li>
        <li><b>Search characters...:</b> Filters the list of known names displayed below.</li>
        <li><b>List Widget:</b> Displays the primary names from your <code>Known.txt</code>. Select entries here to delete them.</li>
        <li><b>Add new show/character name (Input Field):</b> Enter a name or group to add.
            <ul>
                <li><b>Simple Name:</b> e.g., <code>My Awesome Series</code>. Adds as a single entry.</li>
                <li><b>Group for Separate Known.txt Entries:</b> e.g., <code>(Vivi, Ulti, Uta)</code>. Adds "Vivi", "Ulti", and "Uta" as three separate individual entries to <code>Known.txt</code>.</li>
                <li><b>Group for Shared Folder & Single Known.txt Entry (Tilde <code>~</code>):</b> e.g., <code>(Character A, Char A)~</code>. Adds one entry to <code>Known.txt</code> named "Character A Char A". "Character A" and "Char A" become aliases for this single folder/entry.</li>
            </ul>
        </li>
        <li><b>➕ Add Button:</b> Adds the name/group from the input field above to the list and <code>Known.txt</code>.</li>
        <li><b>⤵️ Add to Filter Button:</b>
            <ul>
                <li>Located next to the '➕ Add' button for the 'Known Shows/Characters' list.</li>
                <li>Clicking this button opens a popup window displaying all names from your <code>Known.txt</code> file, each with a checkbox.</li>
                <li>The popup includes a search bar to quickly filter the list of names.</li>
                <li>You can select one or more names using the checkboxes.</li>
                <li>Click 'Add Selected' to insert the chosen names into the 'Filter by Character(s)' input field in the main window.</li>
                <li>If a selected name from <code>Known.txt</code> was originally a group (e.g., defined as <code>(Boa, Hancock)</code> in Known.txt), it will be added to the filter field as <code>(Boa, Hancock)~</code>. Simple names are added as-is.</li>
                <li>'Select All' and 'Deselect All' buttons are available in the popup for convenience.</li>
                <li>Click 'Cancel' to close the popup without any changes.</li>
            </ul>
        </li>
        <li><b>🗑️ Delete Selected Button:</b> Deletes the selected name(s) from the list and <code>Known.txt</code>.</li>
        <li><b>❓ Button (This one!):</b> Displays this comprehensive help guide.</li>
    </ul></body></html>""",
"help_guide_step7_title":"⑦ Log Area & Controls",
"help_guide_step7_content":"""<html><head/><body>
    <h3>Log Area & Controls (Right Panel)</h3>
    <ul>
        <li><b>📜 Progress Log / Extracted Links Log (Label):</b> Title for the main log area; changes if '🔗 Only Links' mode is active.</li>
        <li><b>Search Links... / 🔍 Button (Link Search):</b>
            <ul><li>Visible only when '🔗 Only Links' mode is active. Allows real-time filtering of the extracted links displayed in the main log by text, URL, or platform.</li></ul>
        </li>
        <li><b>Name: [Style] Button (Manga Filename Style):</b>
            <ul><li>Visible only when <b>Manga/Comic Mode</b> is active for a creator feed and not in 'Only Links' or 'Only Archives' mode.</li>
                <li>Cycles through filename styles: <code>Post Title</code>, <code>Original File</code>, <code>Date Based</code>. (See Manga/Comic Mode section for details).</li>
                <li>When 'Original File' or 'Date Based' style is active, an input field for an <b>optional filename prefix</b> will appear next to this button.</li>
            </ul>                
        </li>
        <li><b>Multi-part: [ON/OFF] Button:</b>
            <ul><li>Toggles multi-segment downloads for individual large files.
                <ul><li><b>ON:</b> Can speed up large file downloads (e.g., videos) but may increase UI choppiness or log spam with many small files. An advisory appears when enabling. If a multi-part download fails, it retries as single-stream.</li>
                    <li><b>OFF (Default):</b> Files are downloaded in a single stream.</li>
                </ul>
                <li>Disabled if '🔗 Only Links' or '📦 Only Archives' mode is active.</li>
            </ul>
        </li>
        <li><b>👁️ / 🙈 Button (Log View Toggle):</b> Switches the main log view:
            <ul>
                <li><b>👁️ Progress Log (Default):</b> Shows all download activity, errors, and summaries.</li>
                <li><b>🙈 Missed Character Log:</b> Displays a list of key terms from post titles/content that were skipped due to your 'Filter by Character(s)' settings. Useful for identifying content you might be unintentionally missing.</li>
            </ul>
        </li>
        <li><b>🔄 Reset Button:</b> Clears all input fields, logs, and resets temporary settings to their defaults. Can only be used when no download is active.</li>
        <li><b>Main Log Output (Text Area):</b> Displays detailed progress messages, errors, and summaries. If '🔗 Only Links' mode is active, this area displays the extracted links.</li>
        <li><b>Missed Character Log Output (Text Area):</b> (Viewable via 👁️ / 🙈 toggle) Displays posts/files skipped due to character filters.</li>
        <li><b>External Log Output (Text Area):</b> Appears below the main log if 'Show External Links in Log' is checked. Displays external links found in post descriptions.</li>
        <li><b>Export Links Button:</b>
            <ul><li>Visible and enabled only when '🔗 Only Links' mode is active and links have been extracted.</li>
                <li>Allows you to save all extracted links to a <code>.txt</code> file.</li>
            </ul>
        </li>
        <li><b>Progress: [Status] Label:</b> Shows the overall progress of the download or link extraction process (e.g., posts processed).</li>
        <li><b>File Progress Label:</b> Shows the progress of individual file downloads, including speed and size, or multi-part download status.</li>
    </ul></body></html>""",
"help_guide_step8_title":"⑧ Favorite Mode & Future Features",
"help_guide_step8_content":"""<html><head/><body>
    <h3>Favorite Mode (Downloading from Your Kemono.su Favorites)</h3>
    <p>This mode allows you to download content directly from artists you've favorited on Kemono.su.</p>
    <ul>
        <li><b>⭐ How to Enable:</b>
            <ul>
                <li>Check the <b>'⭐ Favorite Mode'</b> checkbox, located next to the '🔗 Only Links' radio button.</li>
            </ul>
        </li>
        <li><b>UI Changes in Favorite Mode:</b>
            <ul>
                <li>The '🔗 Kemono Creator/Post URL' input area is replaced with a message indicating Favorite Mode is active.</li>
                <li>The standard 'Start Download', 'Pause', 'Cancel' buttons are replaced with:
                    <ul>
                        <li><b>'🖼️ Favorite Artists'</b> button</li>
                        <li><b>'📄 Favorite Posts'</b> button</li>
                    </ul>
                </li>
                <li>The '🍪 Use Cookie' option is automatically enabled and locked, as cookies are required to fetch your favorites.</li>
            </ul>
        </li>
        <li><b>🖼️ Favorite Artists Button:</b>
            <ul>
                <li>Clicking this opens a dialog that lists all artists you have favorited on Kemono.su.</li>
                <li>You can select one or more artists from this list to download their content.</li>
            </ul>
        </li>
        <li><b>📄 Favorite Posts Button (Future Feature):</b>
            <ul>
                <li>Downloading specific favorited <i>posts</i> (especially in a manga-like sequential order if they are part of a series) is a feature currently under development.</li>
                <li>The best way to handle favorited posts, particularly for sequential reading like manga, is still being explored.</li>
                <li>If you have specific ideas or use cases for how you'd like to download and organize favorited posts (e.g., "manga-style" from favorites), please consider opening an issue or joining the discussion on the project's GitHub page. Your input is valuable!</li>
            </ul>
        </li>
        <li><b>Favorite Download Scope (Button):</b>
            <ul>
                <li>This button (next to 'Favorite Posts') controls where content from selected favorite artists is downloaded:
                    <ul>
                        <li><b><i>Scope: Selected Location:</i></b> All selected artists are downloaded into the main 'Download Location' you've set in the UI. Filters apply globally to all content.</li>
                        <li><b><i>Scope: Artist Folders:</i></b> For each selected artist, a subfolder (named after the artist) is automatically created inside your main 'Download Location'. Content for that artist goes into their specific subfolder. Filters apply within each artist's dedicated folder.</li>
                    </ul>
                </li>
            </ul>
        </li>
        <li><b>Filters in Favorite Mode:</b>
            <ul>
                <li>The '🎯 Filter by Character(s)', '🚫 Skip with Words', and 'Filter Files' options you've set in the UI will still apply to the content downloaded from your selected favorite artists.</li>
            </ul>
        </li>
    </ul></body></html>""",
"help_guide_step9_title":"⑨ Key Files & Tour",
"help_guide_step9_content":"""<html><head/><body>
    <h3>Key Files Used by the Application</h3>
    <ul>
        <li><b><code>Known.txt</code>:</b>
            <ul>
                <li>Located in the application's directory (where the <code>.exe</code> or <code>main.py</code> is).</li>
                <li>Stores your list of known shows, characters, or series titles for automatic folder organization when 'Separate Folders by Name/Title' is enabled.</li>
                <li><b>Format:</b>
                    <ul>
                        <li>Each line is an entry.</li>
                        <li><b>Simple Name:</b> e.g., <code>My Awesome Series</code>. Content matching this will go into a folder named "My Awesome Series".</li>
                        <li><b>Grouped Aliases:</b> e.g., <code>(Character A, Char A, Alt Name A)</code>. Content matching "Character A", "Char A", OR "Alt Name A" will ALL go into a single folder named "Character A Char A Alt Name A" (after cleaning). All terms in the parentheses become aliases for that folder.</li>
                    </ul>
                </li>
                <li><b>Usage:</b> Serves as a fallback for folder naming if a post doesn't match your active 'Filter by Character(s)' input. You can manage simple entries via the UI or edit the file directly for complex aliases. The app reloads it on startup or next use.</li>
            </ul>
        </li>
        <li><b><code>cookies.txt</code> (Optional):</b>
            <ul>
                <li>If you use the 'Use Cookie' feature and don't provide a direct cookie string or browse to a specific file, the application will look for a file named <code>cookies.txt</code> in its directory.</li>
                <li><b>Format:</b> Must be in Netscape cookie file format.</li>
                <li><b>Usage:</b> Allows the downloader to use your browser's login session for accessing content that might be behind a login on Kemono/Coomer.</li>
            </ul>
        </li>
    </ul>

    <h3>First-Time User Tour</h3>
    <ul>
        <li>On the first launch (or if reset), a welcome tour dialog appears, guiding you through the main features. You can skip it or choose to "Never show this tour again."</li>
    </ul>
    <p><em>Many UI elements also have tooltips that appear when you hover your mouse over them, providing quick hints.</em></p>
    </body></html>"""
})

translations ["ja"].update ({
"help_guide_dialog_title":"Kemonoダウンローダー - 機能ガイド",
"help_guide_github_tooltip":"プロジェクトのGitHubページにアクセス (ブラウザで開きます)",
"help_guide_instagram_tooltip":"Instagramページにアクセス (ブラウザで開きます)",
"help_guide_discord_tooltip":"Discordコミュニティにアクセス (ブラウザで開きます)",
"help_guide_step1_title":"① 概要と主な入力",
"help_guide_step1_content":"""<html><head/><body>
    <p>このガイドでは、Kemonoダウンローダーの機能、フィールド、ボタンの概要を説明します。</p>
    <h3>メイン入力エリア (左上)</h3>
    <ul>
        <li><b>🔗 Kemonoクリエイター/投稿URL:</b>
            <ul>
                <li>クリエイターのページ（例: <i>https://kemono.su/patreon/user/12345</i>）または特定の投稿（例: <i>.../post/98765</i>）の完全なウェブアドレスを入力します。</li>
                <li>Kemono (kemono.su, kemono.party) および Coomer (coomer.su, coomer.party) のURLをサポートしています。</li>
            </ul>
        </li>
        <li><b>ページ範囲 (開始から終了):</b>
            <ul>
                <li>クリエイターURLの場合: 取得するページの範囲を指定します（例: 2ページから5ページ）。すべてのページを取得する場合は空白のままにします。</li>
                <li>単一の投稿URLまたは<b>マンガ/コミックモード</b>がアクティブな場合は無効になります。</li>
            </ul>
        </li>
        <li><b>📁 ダウンロード場所:</b>
            <ul>
                <li><b>「参照...」</b>をクリックして、ダウンロードしたすべてのファイルが保存されるコンピュータ上のメインフォルダを選択します。</li>
                <li><b>「🔗 リンクのみ」</b>モードを使用している場合を除き、このフィールドは必須です。</li>
            </ul>
        </li>
        <li><b>🎨 クリエイター選択ボタン (URL入力の隣):</b>
            <ul>
                <li>パレットアイコン (🎨) をクリックすると、「クリエイター選択」ダイアログが開きます。</li>
                <li>このダイアログは、<code>creators.json</code>ファイル（アプリケーションのディレクトリにある必要があります）からクリエイターを読み込みます。</li>
                <li><b>ダイアログ内:</b>
                    <ul>
                        <li><b>検索バー:</b> 名前またはサービスでクリエイターのリストをフィルタリングします。</li>
                        <li><b>クリエイターリスト:</b> <code>creators.json</code>ファイルからクリエイターを表示します。JSONデータでお気に入りに登録したクリエイターはリストの上部に表示されます。</li>
                        <li><b>チェックボックス:</b> 名前の隣にあるチェックボックスをオンにして、1人以上のクリエイターを選択します。</li>
                        <li><b>「スコープ」ボタン (例: 「スコープ: キャラクター」):</b> このポップアップからダウンロードを開始する際のダウンロード整理方法を切り替えます:
                            <ul><li><i>スコープ: キャラクター:</i> ダウンロードは、メインの「ダウンロード場所」内に直接キャラクター名のフォルダに整理されます。同じキャラクターの異なるクリエイターのアートは一緒にグループ化されます。</li>
                                <li><i>スコープ: クリエイター:</i> ダウンロードは、まずメインの「ダウンロード場所」内にクリエイター名のフォルダを作成します。その後、各クリエイターのフォルダ内にキャラクター名のサブフォルダが作成されます。</li></ul>
                        </li>
                        <li><b>「選択項目を追加」ボタン:</b> これをクリックすると、チェックされたすべてのクリエイターの名前がメインの「🔗 Kemonoクリエイター/投稿URL」入力フィールドにコンマ区切りで追加され、ダイアログが閉じます。</li>
                    </ul>
                </li>
                <li>この機能は、各URLを手動で入力または貼り付けずに、複数のクリエイターのURLフィールドをすばやく入力する方法を提供します。</li>
            </ul>
        </li>
    </ul></body></html>""",
"help_guide_step2_title":"② ダウンロードのフィルタリング",
"help_guide_step2_content":"""<html><head/><body>
    <h3>ダウンロードのフィルタリング（左パネル）</h3>
    <ul>
        <li><b>🎯 キャラクターでフィルタリング:</b>
            <ul>
                <li>名前をコンマ区切りで入力します（例: <code>ティファ, エアリス</code>）。</li>
                <li><b>共有フォルダ用のグループ化されたエイリアス (個別のKnown.txtエントリ):</b> <code>(ビビ, ウルティ, ウタ)</code>。
                    <ul><li>「ビビ」、「ウルティ」、または「ウタ」に一致するコンテンツは、「ビビ ウルティ ウタ」（クリーニング後）という名前の共有フォルダに入ります。</li>
                        <li>これらの名前が新しい場合、「ビビ」、「ウルティ」、「ウタ」は<code>Known.txt</code>に<i>個別のエントリ</i>として追加するよう促されます。</li>
                    </ul>
                </li>
                <li><b>共有フォルダ用のグループ化されたエイリアス (単一のKnown.txtエントリ):</b> <code>(ユフィ, ソノン)~</code> (チルダ<code>~</code>に注意)。
                    <ul><li>「ユフィ」または「ソノン」に一致するコンテンツは、「ユフィ ソノン」という名前の共有フォルダに入ります。</li>
                        <li>新しい場合、「ユフィ ソノン」(エイリアス: ユフィ, ソノン) は<code>Known.txt</code>に<i>単一のグループエントリ</i>として追加するよう促されます。</li>
                    </ul>
                </li>
                <li>「名前/タイトルでフォルダを分ける」が有効な場合、このフィルターはフォルダ名にも影響します。</li>
            </ul>
        </li>
        <li><b>フィルター: [タイプ] ボタン (キャラクターフィルタースコープ):</b> 「キャラクターでフィルタリング」の適用方法を循環します:
            <ul>
                <li><code>フィルター: ファイル</code>: 個々のファイル名を確認します。いずれかのファイルが一致すれば投稿は保持され、一致するファイルのみがダウンロードされます。フォルダ名は一致するファイル名のキャラクターを使用します。</li>
                <li><code>フィルター: タイトル</code>: 投稿タイトルを確認します。一致する投稿のすべてのファイルがダウンロードされます。フォルダ名は一致する投稿タイトルのキャラクターを使用します。</li>
                <li><code>フィルター: 両方</code>: まず投稿タイトルを確認します。一致する場合、すべてのファイルがダウンロードされます。一致しない場合、次にファイル名を確認し、一致するファイルのみがダウンロードされます。フォルダ名はタイトル一致を優先し、次にファイル一致を優先します。</li>
                <li><code>フィルター: コメント (ベータ)</code>: まずファイル名を確認します。ファイルが一致する場合、投稿のすべてのファイルがダウンロードされます。ファイル一致がない場合、次に投稿コメントを確認します。コメントが一致する場合、投稿のすべてのファイルがダウンロードされます。(より多くのAPIリクエストを使用します)。フォルダ名はファイル一致を優先し、次にコメント一致を優先します。</li>
            </ul>
        </li>
        <li><b>🗄️ カスタムフォルダ名 (単一投稿のみ):</b>
            <ul>
                <li>単一の特定の投稿URLをダウンロードしていて、かつ「名前/タイトルでフォルダを分ける」が有効な場合にのみ表示され、使用可能です。</li>
                <li>その単一投稿のダウンロードフォルダにカスタム名を指定できます。</li>
            </ul>
        </li>
        <li><b>🚫 スキップする単語:</b>
            <ul><li>特定のコンテンツをスキップするために、単語をコンマ区切りで入力します（例: <code>WIP, スケッチ, プレビュー</code>）。</li></ul>
        </li>
        <li><b>スコープ: [タイプ] ボタン (スキップワードスコープ):</b> 「スキップする単語」の適用方法を循環します:
            <ul>
                <li><code>スコープ: ファイル</code>: 名前にこれらの単語のいずれかを含む場合、個々のファイルをスキップします。</li>
                <li><code>スコープ: 投稿</code>: タイトルにこれらの単語のいずれかを含む場合、投稿全体をスキップします。</li>
                <li><code>スコープ: 両方</code>: 両方を適用します（まず投稿タイトル、次に個々のファイル）。</li>
            </ul>
        </li>
        <li><b>✂️ 名前から単語を削除:</b>
            <ul><li>ダウンロードしたファイル名から削除する単語をコンマ区切りで入力します（大文字と小文字を区別しません）（例: <code>patreon, [HD]</code>）。</li></ul>
        </li>
        <li><b>ファイルフィルター (ラジオボタン):</b> ダウンロードするものを選択します:
            <ul>
                <li><code>すべて</code>: 見つかったすべてのファイルタイプをダウンロードします。</li>
                <li><code>画像/GIF</code>: 一般的な画像形式（JPG, PNG, GIF, WEBPなど）とGIFのみ。</li>
                <li><code>動画</code>: 一般的な動画形式（MP4, MKV, WEBM, MOVなど）のみ。</li>
                <li><code>📦 アーカイブのみ</code>: <b>.zip</b>と<b>.rar</b>ファイルのみをダウンロードします。選択すると、「.zipをスキップ」と「.rarをスキップ」チェックボックスは自動的に無効になり、チェックが外れます。「外部リンクをログに表示」も無効になります。</li>
                <li><code>🎧 音声のみ</code>: 一般的な音声形式（MP3, WAV, FLAC, M4A, OGGなど）のみダウンロードします。他のファイル固有のオプションは、「画像」または「動画」モードと同様に動作します。</li>
                <li><code>🔗 リンクのみ</code>: ファイルをダウンロードする代わりに、投稿の説明から外部リンクを抽出して表示します。ダウンロード関連のオプションと「外部リンクをログに表示」は無効になります。メインのダウンロードボタンは「🔗 リンクを抽出」に変わります。</li>                    
            </ul>
        </li>
    </ul></body></html>""",
"help_guide_step3_title":"③ ダウンロードオプションと設定",
"help_guide_step3_content":"""<html><head/><body>
    <h3>ダウンロードオプションと設定（左パネル）</h3>
    <ul>
        <li><b>.zipをスキップ / .rarをスキップ:</b> これらのアーカイブファイルタイプをダウンロードしないようにするためのチェックボックス。(「📦 アーカイブのみ」フィルターモードが選択されている場合は無効になり、無視されます)。</li>
        <li><b>サムネイルのみダウンロード:</b> フルサイズのファイルの代わりに小さなプレビュー画像をダウンロードします（利用可能な場合）。</li>
        <li><b>大きな画像を圧縮 (WebPへ):</b> 「Pillow」(PIL) ライブラリがインストールされている場合、1.5MBより大きい画像は、WebPバージョンが大幅に小さい場合にWebP形式に変換されます。</li>
        <li><b>⚙️ 詳細設定:</b>
            <ul>
                <li><b>名前/タイトルでフォルダを分ける:</b> 「キャラクターでフィルタリング」入力または投稿タイトルに基づいてサブフォルダを作成します。<b>Known.txt</b>リストをフォルダ名のフォールバックとして使用できます。</li></ul></li></ul></body></html>""",
"help_guide_step4_title":"④ 詳細設定（その1）",
"help_guide_step4_content":"""<html><head/><body><h3>⚙️ 詳細設定（続き）</h3><ul><ul>
                <li><b>投稿ごとにサブフォルダ:</b> 「フォルダを分ける」がオンの場合、メインのキャラクター/タイトルフォルダ内に<i>個々の投稿</i>ごとに追加のサブフォルダを作成します。</li>
                <li><b>Cookieを使用:</b> リクエストにCookieを使用するには、これをチェックします。
                    <ul>
                        <li><b>テキストフィールド:</b> Cookie文字列を直接入力します（例: <code>name1=value1; name2=value2</code>）。</li>
                        <li><b>参照...:</b> <code>cookies.txt</code>ファイル（Netscape形式）を選択します。パスがテキストフィールドに表示されます。</li>
                        <li><b>優先順位:</b> テキストフィールド (入力されている場合) が参照されたファイルよりも優先されます。「Cookieを使用」がチェックされていて両方が空の場合、アプリのディレクトリから<code>cookies.txt</code>を読み込もうとします。</li>
                    </ul>
                </li>
                <li><b>マルチスレッドを使用 & スレッド数入力:</b>
                    <ul>
                        <li>より高速な操作を可能にします。「スレッド数」入力の数値の意味:
                            <ul>
                                <li><b>クリエイターフィードの場合:</b> 同時に処理する投稿の数。各投稿内のファイルは、そのワーカーによって順番にダウンロードされます（「日付順」マンガ命名がオンの場合を除く。これは1つの投稿ワーカーを強制します）。</li>
                                <li><b>単一投稿URLの場合:</b> その単一投稿から同時にダウンロードするファイルの数。</li>
                            </ul>
                        </li>
                        <li>チェックされていない場合、1スレッドが使用されます。高いスレッド数（例: >40）はアドバイザリを表示する場合があります。</li>
                    </ul>
                </li></ul></ul></body></html>""",
"help_guide_step5_title":"⑤ 詳細設定（その2）とアクション",
"help_guide_step5_content":"""<html><head/><body><h3>⚙️ 詳細設定（続き）</h3><ul><ul>
                <li><b>ログに外部リンクを表示:</b> チェックすると、メインログの下にセカンダリログパネルが表示され、投稿の説明で見つかった外部リンクが表示されます。(「🔗 リンクのみ」または「📦 アーカイブのみ」モードがアクティブな場合は無効になります)。</li>
                <li><b>📖 マンガ/コミックモード (クリエイターURLのみ):</b> シーケンシャルコンテンツ向けに調整されています。
                    <ul>
                        <li>投稿を<b>古いものから新しいものへ</b>ダウンロードします。</li>
                        <li>すべての投稿が取得されるため、「ページ範囲」入力は無効になります。</li>
                        <li>このモードがクリエイターフィードでアクティブな場合、ログエリアの右上に<b>ファイル名スタイル切り替えボタン</b>（例: 「名前: 投稿タイトル」）が表示されます。クリックすると命名スタイルが循環します:
                            <ul>
                                <li><code>名前: 投稿タイトル (デフォルト)</code>: 投稿の最初のファイルは、投稿のクリーンなタイトルにちなんで名付けられます（例: 「My Chapter 1.jpg」）。*同じ投稿*内の後続のファイルは、元のファイル名を保持しようとします（例: 「page_02.png」、「bonus_art.jpg」）。投稿にファイルが1つしかない場合は、投稿タイトルにちなんで名付けられます。これはほとんどのマンガ/コミックに一般的に推奨されます。</li>
                                <li><code>名前: 元ファイル名</code>: すべてのファイルが元のファイル名を保持しようとします。</li>
                                <li><code>名前: 元ファイル名</code>: すべてのファイルが元のファイル名を保持しようとします。このスタイルがアクティブな場合、オプションのファイル名プレフィックス（例: 「MySeries_」）をこのスタイルボタンの隣に表示される入力フィールドに入力できます。例: 「MySeries_OriginalFile.jpg」。</li>
                                <li><code>名前: タイトル+通し番号 (投稿タイトル+グローバル番号付け)</code>: 現在のダウンロードセッションのすべての投稿のすべてのファイルが、投稿のクリーンなタイトルをプレフィックスとして使用し、グローバルカウンターを続けて順番に名付けられます。例: 投稿「Chapter 1」（2ファイル）-> 「Chapter 1 001.jpg」、「Chapter 1 002.png」。次の投稿「Chapter 2」（1ファイル）は番号付けを続けます -> 「Chapter 2 003.jpg」。このスタイルの場合、正しいグローバル番号付けを保証するために、投稿処理のマルチスレッドは自動的に無効になります。</li>
                                <li><code>名前: 日付順</code>: ファイルは投稿の公開順に基づいて順番に名付けられます（001.ext、002.extなど）。このスタイルがアクティブな場合、オプションのファイル名プレフィックス（例: 「MySeries_」）をこのスタイルボタンの隣に表示される入力フィールドに入力できます。例: 「MySeries_001.jpg」。このスタイルの場合、投稿処理のマルチスレッドは自動的に無効になります。</li>
                            </ul>
                        </li>
                        <li>「名前: 投稿タイトル」、「名前: タイトル+通し番号」、または「名前: 日付順」スタイルで最良の結果を得るには、「キャラクターでフィルタリング」フィールドにマンガ/シリーズのタイトルを入力してフォルダを整理します。</li>
                    </ul>
                </li>
            </ul></li></ul>
    
    <h3>メインアクションボタン（左パネル）</h3>
    <ul>
        <li><b>⬇️ ダウンロード開始 / 🔗 リンクを抽出:</b> このボタンのテキストと機能は、「ファイルフィルター」ラジオボタンの選択に基づいて変わります。主要な操作を開始します。</li>
        <li><b>⏸️ 一時停止 / ▶️ 再開:</b> 現在のダウンロード/抽出プロセスを一時的に停止し、後で再開できます。一時停止中に一部のUI設定を変更できます。</li>
        <li><b>❌ 中止してUIリセット:</b> 現在の操作を停止し、ソフトUIリセットを実行します。URLとダウンロードディレクトリ入力は保持されますが、他の設定とログはクリアされます。</li>
    </ul></body></html>""",
"help_guide_step6_title":"⑥ 既知の番組/キャラクターリスト",
"help_guide_step6_content":"""<html><head/><body>
    <h3>既知の番組/キャラクターリスト管理（左下）</h3>
    <p>このセクションは、<code>Known.txt</code>ファイルの管理に役立ちます。このファイルは、「名前/タイトルでフォルダを分ける」が有効な場合にスマートなフォルダ整理に使用され、特に投稿がアクティブな「キャラクターでフィルタリング」入力に一致しない場合のフォールバックとして機能します。</p>
    <ul>
        <li><b>Known.txtを開く:</b> <code>Known.txt</code>ファイル（アプリのディレクトリにあります）をデフォルトのテキストエディタで開き、高度な編集（複雑なグループ化されたエイリアスの作成など）を行います。</li>
        <li><b>キャラクターを検索...:</b> 以下に表示される既知の名前のリストをフィルタリングします。</li>
        <li><b>リストウィジェット:</b> <code>Known.txt</code>からプライマリ名を表示します。削除するエントリをここで選択します。</li>
        <li><b>新しい番組/キャラクター名を追加 (入力フィールド):</b> 追加する名前またはグループを入力します。
            <ul>
                <li><b>単純な名前:</b> 例: <code>My Awesome Series</code>。単一のエントリとして追加されます。</li>
                <li><b>個別のKnown.txtエントリ用のグループ:</b> 例: <code>(ビビ, ウルティ, ウタ)</code>。「ビビ」、「ウルティ」、「ウタ」が3つの個別のエントリとして<code>Known.txt</code>に追加されます。</li>
                <li><b>共有フォルダ & 単一Known.txtエントリ用のグループ (チルダ<code>~</code>):</b> 例: <code>(キャラクターA, キャラA)~</code>。「キャラクターA キャラA」という名前の1つのエントリが<code>Known.txt</code>に追加されます。「キャラクターA」と「キャラA」がこの単一フォルダ/エントリのエイリアスになります。</li>
            </ul>
        </li>
        <li><b>➕ 追加ボタン:</b> 上の入力フィールドの名前/グループをリストと<code>Known.txt</code>に追加します。</li>
        <li><b>⤵️ フィルターに追加ボタン:</b>
            <ul>
                <li>「既知の番組/キャラクター」リストの「➕ 追加」ボタンの隣にあります。</li>
                <li>これをクリックすると、<code>Known.txt</code>ファイルのすべての名前がチェックボックス付きで表示されるポップアップウィンドウが開きます。</li>
                <li>ポップアップには、名前のリストをすばやくフィルタリングするための検索バーが含まれています。</li>
                <li>チェックボックスを使用して1つ以上の名前を選択できます。</li>
                <li>「選択項目を追加」をクリックすると、選択した名前がメインウィンドウの「キャラクターでフィルタリング」入力フィールドに挿入されます。</li>
                <li><code>Known.txt</code>から選択した名前が元々グループだった場合（例: Known.txtで<code>(ボア, ハンコック)</code>と定義されていた場合）、フィルターフィールドに<code>(ボア, ハンコック)~</code>として追加されます。単純な名前はそのまま追加されます。</li>
                <li>ポップアップには、「すべて選択」と「すべて選択解除」ボタンが便宜上用意されています。</li>
                <li>「キャンセル」をクリックすると、変更なしでポップアップが閉じます。</li>
            </ul>
        </li>
        <li><b>🗑️ 選択項目を削除ボタン:</b> 選択した名前をリストと<code>Known.txt</code>から削除します。</li>
        <li><b>❓ ボタン（これです！):</b> この包括的なヘルプガイドを表示します。</li>
    </ul></body></html>""",
"help_guide_step7_title":"⑦ ログエリアとコントロール",
"help_guide_step7_content":"""<html><head/><body>
    <h3>ログエリアとコントロール（右パネル）</h3>
    <ul>
        <li><b>📜 進捗ログ / 抽出リンクログ (ラベル):</b> メインログエリアのタイトル。「🔗 リンクのみ」モードがアクティブな場合は変わります。</li>
        <li><b>リンクを検索... / 🔍 ボタン (リンク検索):</b>
            <ul><li>「🔗 リンクのみ」モードがアクティブな場合にのみ表示されます。メインログに表示される抽出されたリンクをテキスト、URL、またはプラットフォームでリアルタイムにフィルタリングできます。</li></ul>
        </li>
        <li><b>名前: [スタイル] ボタン (マンガファイル名スタイル):</b>
            <ul><li><b>マンガ/コミックモード</b>がクリエイターフィードでアクティブで、かつ「🔗 リンクのみ」または「📦 アーカイブのみ」モードでない場合にのみ表示されます。</li>
                <li>ファイル名スタイルを循環します: <code>投稿タイトル</code>、<code>元ファイル名</code>、<code>日付順</code>。（詳細はマンガ/コミックモードのセクションを参照）。</li>
                <li>「元ファイル名」または「日付順」スタイルがアクティブな場合、オプションのファイル名プレフィックス用の入力フィールドがこのスタイルボタンの隣に表示されます。</li>
            </ul>                
        </li>
        <li><b>マルチパート: [オン/オフ] ボタン:</b>
            <ul><li>個々の大きなファイルのマルチセグメントダウンロードを切り替えます。
                <ul><li><b>オン:</b> 大きなファイルのダウンロード（例: 動画）を高速化できますが、多くの小さなファイルがある場合、UIの途切れやログのスパムが増加する可能性があります。有効にするとアドバイザリが表示されます。マルチパートダウンロードが失敗した場合、シングルストリームで再試行します。</li>
                    <li><b>オフ（デフォルト）:</b> ファイルは単一のストリームでダウンロードされます。</li>
                </ul>
                <li>「🔗 リンクのみ」または「📦 アーカイブのみ」モードがアクティブな場合は無効になります。</li>
            </ul>
        </li>
        <li><b>👁️ / 🙈 ボタン (ログビュー切り替え):</b> メインログビューを切り替えます:
            <ul>
                <li><b>👁️ 進捗ログ（デフォルト）:</b> すべてのダウンロードアクティビティ、エラー、概要を表示します。</li>
                <li><b>🙈 見逃したキャラクターログ:</b> 「キャラクターでフィルタリング」設定のためにスキップされた投稿タイトル/コンテンツのキーワードのリストを表示します。意図せずに見逃している可能性のあるコンテンツを特定するのに役立ちます。</li>
            </ul>
        </li>
        <li><b>🔄 リセットボタン:</b> すべての入力フィールド、ログをクリアし、一時的な設定をデフォルトにリセットします。ダウンロードがアクティブでない場合にのみ使用できます。</li>
        <li><b>メインログ出力 (テキストエリア):</b> 詳細な進捗メッセージ、エラー、概要を表示します。「🔗 リンクのみ」モードがアクティブな場合、このエリアには抽出されたリンクが表示されます。</li>
        <li><b>見逃したキャラクターログ出力 (テキストエリア):</b> （👁️ / 🙈 切り替えで表示可能）キャラクターフィルターのためにスキップされた投稿/ファイルを表示します。</li>
        <li><b>外部リンク出力 (テキストエリア):</b> 「ログに外部リンクを表示」がチェックされている場合、メインログの下に表示されます。投稿の説明で見つかった外部リンクを表示します。</li>
        <li><b>リンクをエクスポートボタン:</b>
            <ul><li>「🔗 リンクのみ」モードがアクティブで、リンクが抽出されている場合にのみ表示され、有効になります。</li>
                <li>抽出されたすべてのリンクを<code>.txt</code>ファイルに保存できます。</li>
            </ul>
        </li>
        <li><b>進捗: [ステータス] ラベル:</b> ダウンロードまたはリンク抽出プロセスの全体的な進捗（例: 処理済み投稿）を表示します。</li>
        <li><b>ファイル進捗ラベル:</b> 個々のファイルダウンロードの進捗（速度とサイズを含む）またはマルチパートダウンロードのステータスを表示します。</li>
    </ul></body></html>""",
"help_guide_step8_title":"⑧ お気に入りモードと将来の機能",
"help_guide_step8_content":"""<html><head/><body>
    <h3>お気に入りモード（Kemono.su/Coomer.suのお気に入りからダウンロード）</h3>
    <p>このモードでは、Kemono.suでお気に入りに登録したアーティストから直接コンテンツをダウンロードできます。</p>
    <ul>
        <li><b>⭐ 有効にする方法:</b>
            <ul>
                <li>「🔗 リンクのみ」ラジオボタンの隣にある<b>「⭐ お気に入りモード」</b>チェックボックスをオンにします。</li>
            </ul>
        </li>
        <li><b>お気に入りモードでのUIの変更:</b>
            <ul>
                <li>「🔗 Kemonoクリエイター/投稿URL」入力エリアは、お気に入りモードがアクティブであることを示すメッセージに置き換えられます。</li>
                <li>標準の「ダウンロード開始」、「一時停止」、「キャンセル」ボタンは、以下に置き換えられます:
                    <ul>
                        <li><b>「🖼️ お気に入りアーティスト」</b>ボタン</li>
                        <li><b>「📄 お気に入り投稿」</b>ボタン</li>
                    </ul>
                </li>
                <li>お気に入りを取得するにはCookieが必要なため、「🍪 Cookieを使用」オプションは自動的に有効になり、ロックされます。</li>
            </ul>
        </li>
        <li><b>🖼️ お気に入りアーティストボタン:</b>
            <ul>
                <li>これをクリックすると、Kemono.suでお気に入りに登録したすべてのアーティストのリストが表示されるダイアログが開きます。</li>
                <li>このリストから1人以上のアーティストを選択して、コンテンツをダウンロードできます。</li>
            </ul>
        </li>
        <li><b>📄 お気に入り投稿ボタン (将来の機能):</b>
            <ul>
                <li>特定のお気に入り<i>投稿</i>のダウンロード（特にシリーズの一部である場合のマンガのようなシーケンシャルな順序でのダウンロード）は、現在開発中の機能です。</li>
                <li>お気に入りの投稿、特にマンガのようなシーケンシャルな読書のための最適な処理方法は、まだ検討中です。</li>
                <li>お気に入りの投稿をダウンロードして整理する方法（例: お気に入りからの「マンガスタイル」）について具体的なアイデアやユースケースがある場合は、プロジェクトのGitHubページでイシューを開くか、ディスカッションに参加することを検討してください。あなたの意見は貴重です！</li>
            </ul>
        </li>
        <li><b>お気に入りダウンロードスコープ (ボタン):</b>
            <ul>
                <li>このボタン（「お気に入り投稿」の隣）は、選択したお気に入りアーティストのコンテンツのダウンロード場所を制御します:
                    <ul>
                        <li><b><i>スコープ: 選択場所:</i></b> 選択したすべてのアーティストは、UIで設定したメインの「ダウンロード場所」にダウンロードされます。フィルターはすべてのコンテンツにグローバルに適用されます。</li>
                        <li><b><i>スコープ: アーティストフォルダ:</i></b> 選択した各アーティストについて、メインの「ダウンロード場所」内にサブフォルダ（アーティスト名）が自動的に作成されます。そのアーティストのコンテンツは、特定のサブフォルダにダウンロードされます。フィルターは各アーティストの専用フォルダ内で適用されます。</li>
                    </ul>
                </li>
            </ul>
        </li>
        <li><b>お気に入りモードでのフィルター:</b>
            <ul>
                <li>UIで設定した「🎯 キャラクターでフィルタリング」、「🚫 スキップする単語」、「ファイルフィルター」オプションは、選択したお気に入りアーティストからダウンロードされるコンテンツにも適用されます。</li>
            </ul>
        </li>
    </ul></body></html>""",
"help_guide_step9_title":"⑨ 主要ファイルとツアー",
"help_guide_step9_content":"""<html><head/><body>
    <h3>アプリケーションが使用するキーファイル</h3>
    <ul>
        <li><b><code>Known.txt</code>:</b>
            <ul>
                <li>アプリケーションのディレクトリ（<code>.exe</code>または<code>main.py</code>がある場所）にあります。</li>
                <li>「名前/タイトルでフォルダを分ける」が有効な場合に、自動フォルダ整理のために既知の番組、キャラクター、またはシリーズタイトルのリストを保存します。</li>
                <li><b>形式:</b>
                    <ul>
                        <li>各行がエントリです。</li>
                        <li><b>単純な名前:</b> 例: <code>My Awesome Series</code>。これに一致するコンテンツは「My Awesome Series」という名前のフォルダに入ります。</li>
                        <li><b>グループ化されたエイリアス:</b> 例: <code>(キャラクターA, キャラA, 別名A)</code>。「キャラクターA」、「キャラA」、または「別名A」に一致するコンテンツはすべて、「キャラクターA キャラA 別名A」（クリーニング後）という名前の単一フォルダに入ります。括弧内のすべての用語がそのフォルダのエイリアスになります。</li>
                    </ul>
                </li>
                <li><b>使用法:</b> 投稿がアクティブな「キャラクターでフィルタリング」入力に一致しない場合のフォルダ名のフォールバックとして機能します。UIから単純なエントリを管理したり、複雑なエイリアスを作成するためにファイルを直接編集したりできます。アプリは起動時または次回使用時に再読み込みします。</li>
            </ul>
        </li>
        <li><b><code>cookies.txt</code> (オプション):</b>
            <ul>
                <li>「Cookieを使用」機能を使用し、直接Cookie文字列を提供しないか、特定のファイルを参照しない場合、アプリケーションはそのディレクトリにある<code>cookies.txt</code>という名前のファイルを探します。</li>
                <li><b>形式:</b> Netscape Cookieファイル形式である必要があります。</li>
                <li><b>使用法:</b> ダウンローダーがブラウザのログインセッションを使用して、Kemono/Coomerでログインが必要な可能性のあるコンテンツにアクセスできるようにします。</li>
            </ul>
        </li>
    </ul>

    <h3>初回ユーザーツアー</h3>
    <ul>
        <li>初回起動時（またはリセット時）に、主な機能を案内するウェルカムツアーダイアログが表示されます。スキップするか、「今後このツアーを表示しない」を選択できます。</li>
    </ul>
    <p><em>多くのUI要素には、マウスオーバーするとクイックヒントが表示されるツールチップもあります。</em></p>
    </body></html>"""
})

translations ["zh_CN"]={}
translations ["zh_CN"].update ({
"settings_dialog_title":"设置",
"language_label":"语言：",
"lang_english":"英语 (English)",
"lang_japanese":"日语 (日本語)",
"theme_toggle_light":"切换到浅色模式",
"theme_toggle_dark":"切换到深色模式",
"theme_tooltip_light":"将应用程序外观更改为浅色。",
"theme_tooltip_dark":"将应用程序外观更改为深色。",
"ok_button":"确定",
"appearance_group_title":"外观",
"language_group_title":"语言设置",
"creator_post_url_label":"🔗 Kemono 作者/帖子 URL：",
"download_location_label":"📁 下载位置：",
"filter_by_character_label":"🎯 按角色筛选 (逗号分隔)：",
"skip_with_words_label":"🚫 使用关键词跳过 (逗号分隔)：",
"remove_words_from_name_label":"✂️ 从名称中删除词语：",
"filter_all_radio":"全部",
"filter_images_radio":"图片/GIF",
"filter_videos_radio":"视频",
"filter_archives_radio":"📦 仅存档",
"filter_links_radio":"🔗 仅链接",
"filter_audio_radio":"🎧 仅音频",
"favorite_mode_checkbox_label":"⭐ 收藏模式",
"browse_button_text":"浏览...",
"char_filter_scope_files_text":"筛选：文件",
"char_filter_scope_files_tooltip":"当前范围：文件\n\n按文件名筛选单个文件。如果任何文件匹配，则保留帖子。\n只下载该帖子中匹配的文件。\n示例：筛选“Tifa”。文件“Tifa_artwork.jpg”匹配并被下载。\n文件夹命名：使用匹配文件名中的角色。\n\n点击切换到：两者",
"char_filter_scope_title_text":"筛选：标题",
"char_filter_scope_title_tooltip":"当前范围：标题\n\n按帖子标题筛选整个帖子。匹配帖子的所有文件都将被下载。\n示例：筛选“Aerith”。标题为“Aerith's Garden”的帖子匹配；其所有文件都将被下载。\n文件夹命名：使用匹配帖子标题中的角色。\n\n点击切换到：文件",
"char_filter_scope_both_text":"筛选：两者",
"char_filter_scope_both_tooltip":"当前范围：两者 (标题优先，然后是文件)\n\n1. 检查帖子标题：如果匹配，则下载帖子中的所有文件。\n2. 如果标题不匹配，则检查文件名：如果任何文件匹配，则仅下载该文件。\n示例：筛选“Cloud”。\n - 帖子“Cloud Strife”(标题匹配) -> 所有文件都被下载。\n - 帖子“Bike Chase”中包含“Cloud_fenrir.jpg”(文件匹配) -> 仅下载“Cloud_fenrir.jpg”。\n文件夹命名：优先考虑标题匹配，然后是文件匹配。\n\n点击切换到：评论",
"char_filter_scope_comments_text":"筛选：评论 (测试版)",
"char_filter_scope_comments_tooltip":"当前范围：评论 (测试版 - 文件优先，然后是评论作为后备)\n\n1. 检查文件名：如果帖子中的任何文件与筛选器匹配，则下载整个帖子。评论不会针对此筛选词进行检查。\n2. 如果没有文件匹配，则检查帖子评论：如果评论匹配，则下载整个帖子。\n示例：筛选“Barret”。\n - 帖子 A：文件“Barret_gunarm.jpg”、“other.png”。文件“Barret_gunarm.jpg”匹配。帖子 A 的所有文件都被下载。评论中不会检查“Barret”。\n - 帖子 B：文件“dyne.jpg”、“weapon.gif”。评论：“...一张 Barret Wallace 的画...”。没有文件匹配“Barret”。评论匹配。帖子 B 的所有文件都被下载。\n文件夹命名：优先考虑文件匹配中的角色，然后是评论匹配中的角色。\n\n点击切换到：标题",
"char_filter_scope_unknown_text":"筛选：未知",
"char_filter_scope_unknown_tooltip":"当前范围：未知\n\n角色筛选范围处于未知状态。请循环或重置。\n\n点击切换到：标题",
"skip_words_input_tooltip":"输入词语，以逗号分隔，以跳过下载某些内容（例如，WIP、sketch、preview）。\n\n此输入旁边的“范围：[类型]”按钮可循环此筛选器的应用方式：\n- 范围：文件：如果文件名包含任何这些词语，则跳过单个文件。\n- 范围：帖子：如果帖子标题包含任何这些词语，则跳过整个帖子。\n- 范围：两者：同时应用两者（首先是帖子标题，如果帖子标题可以，则应用单个文件）。",
"remove_words_input_tooltip":"输入词语，以逗号分隔，以从下载的文件名中删除（不区分大小写）。\n用于清理常见的前缀/后缀。\n示例：patreon、kemono、[HD]、_final",
"skip_scope_files_text":"范围：文件",
"skip_scope_files_tooltip":"当前跳过范围：文件\n\n如果文件名包含任何“要跳过的词语”，则跳过单个文件。\n示例：跳过词语“WIP，sketch”。\n- 文件“art_WIP.jpg”-> 已跳过。\n- 文件“final_art.png”-> 已下载（如果满足其他条件）。\n\n帖子仍会处理其他未跳过的文件。\n点击切换到：两者",
"skip_scope_posts_text":"范围：帖子",
"skip_scope_posts_tooltip":"当前跳过范围：帖子\n\n如果帖子标题包含任何“要跳过的词语”，则跳过整个帖子。\n跳过的帖子中的所有文件都将被忽略。\n示例：跳过词语“preview，announcement”。\n- 帖子“激动人心的公告！”-> 已跳过。\n- 帖子“完成的艺术品”-> 已处理（如果满足其他条件）。\n\n点击切换到：文件",
"skip_scope_both_text":"范围：两者",
"skip_scope_both_tooltip":"当前跳过范围：两者（帖子优先，然后是文件）\n\n1. 检查帖子标题：如果标题包含跳过词语，则整个帖子被跳过。\n2. 如果帖子标题可以，则检查单个文件名：如果文件名包含跳过词语，则仅跳过该文件。\n示例：跳过词语“WIP，sketch”。\n- 帖子“草图和WIPs”（标题匹配）-> 整个帖子被跳过。\n- 帖子“艺术更新”（标题可以），包含文件：\n- “character_WIP.jpg”（文件匹配）-> 已跳过。\n- “final_scene.png”（文件可以）-> 已下载。\n\n点击切换到：帖子",
"skip_scope_unknown_text":"范围：未知",
"skip_scope_unknown_tooltip":"当前跳过范围：未知\n\n跳过词语的范围处于未知状态。请循环或重置。\n\n点击切换到：帖子",
"language_change_title":"语言已更改",
"language_change_message":"语言已更改。需要重新启动才能使所有更改完全生效。",
"language_change_informative":"您想现在重新启动应用程序吗？",
"restart_now_button":"立即重启",
"skip_zip_checkbox_label":"跳过 .zip",
"skip_rar_checkbox_label":"跳过 .rar",
"download_thumbnails_checkbox_label":"仅下载缩略图",
"scan_content_images_checkbox_label":"扫描内容中的图片",
"compress_images_checkbox_label":"压缩为 WebP",
"separate_folders_checkbox_label":"按名称/标题分文件夹",
"subfolder_per_post_checkbox_label":"每篇帖子一个子文件夹",
"use_cookie_checkbox_label":"使用 Cookie",
"use_multithreading_checkbox_base_label":"使用多线程",
"show_external_links_checkbox_label":"在日志中显示外部链接",
"manga_comic_mode_checkbox_label":"漫画/动漫模式",
"threads_label":"线程数：",
"start_download_button_text":"⬇️ 开始下载",
"start_download_button_tooltip":"点击以使用当前设置开始下载或链接提取过程。",
"extract_links_button_text":"🔗 提取链接",
"pause_download_button_text":"⏸️ 暂停下载",
"pause_download_button_tooltip":"点击以暂停正在进行的下载过程。",
"resume_download_button_text":"▶️ 继续下载",
"resume_download_button_tooltip":"点击以继续下载。",
"cancel_button_text":"❌ 取消并重置界面",
"cancel_button_tooltip":"点击以取消正在进行的下载/提取过程并重置界面字段（保留 URL 和目录）。",
"error_button_text":"错误",
"error_button_tooltip":"查看因错误而跳过的文件，并可选择重试。",
"cancel_retry_button_text":"❌ 取消重试",
"known_chars_label_text":"🎭 已知系列/角色（用于文件夹名称）：",
"open_known_txt_button_text":"打开 Known.txt",
"known_chars_list_tooltip":"此列表包含在启用“分文件夹”且未提供或未匹配帖子的特定“按角色筛选”时用于自动创建文件夹的名称。\n添加您经常下载的系列、游戏或角色的名称。",
"open_known_txt_button_tooltip":"在您的默认文本编辑器中打开“Known.txt”文件。\n该文件位于应用程序的目录中。",
"add_char_button_text":"➕ 添加",
"add_char_button_tooltip":"将输入字段中的名称添加到“已知系列/角色”列表中。",
"add_to_filter_button_text":"⤵️ 添加到筛选器",
"add_to_filter_button_tooltip":"从“已知系列/角色”列表中选择名称以添加到上面的“按角色筛选”字段。",
"delete_char_button_text":"🗑️ 删除所选",
"delete_char_button_tooltip":"从“已知系列/角色”列表中删除所选的名称。",
"progress_log_label_text":"📜 进度日志：",
"radio_all_tooltip":"下载帖子中找到的所有文件类型。",
"radio_images_tooltip":"仅下载常见的图像格式（JPG、PNG、GIF、WEBP 等）。",
"radio_videos_tooltip":"仅下载常见的视频格式（MP4、MKV、WEBM、MOV 等）。",
"radio_only_archives_tooltip":"专门下载 .zip 和 .rar 文件。其他特定于文件的选项将被禁用。",
"radio_only_audio_tooltip":"仅下载常见的音频格式（MP3、WAV、FLAC 等）。",
"radio_only_links_tooltip":"从帖子描述中提取并显示外部链接，而不是下载文件。\n与下载相关的选项将被禁用。",
"favorite_mode_checkbox_tooltip":"启用收藏模式以浏览已保存的艺术家/帖子。\n这将用收藏选择按钮替换 URL 输入。",
"skip_zip_checkbox_tooltip":"如果选中，将不下载 .zip 存档文件。\n（如果选择了“仅存档”，则禁用）。",
"skip_rar_checkbox_tooltip":"如果选中，将不下载 .rar 存档文件。\n（如果选择了“仅存档”，则禁用）。",
"download_thumbnails_checkbox_tooltip":"下载 API 中的小预览图像，而不是全尺寸文件（如果可用）。\n如果还选中了“扫描帖子内容以查找图像 URL”，则此模式将*仅*下载内容扫描找到的图像（忽略 API 缩略图）。",
"scan_content_images_checkbox_tooltip":"如果选中，下载器将扫描帖子的 HTML 内容以查找图像 URL（来自 <img> 标签或直接链接）。\n这包括将 <img> 标签中的相对路径解析为完整 URL。\n<img> 标签中的相对路径（例如，/data/image.jpg）将被解析为完整 URL。\n在图像位于帖子描述中但不在 API 的文件/附件列表中的情况下很有用。",
"compress_images_checkbox_tooltip":"将大于 1.5MB 的图像压缩为 WebP 格式（需要 Pillow）。",
"use_subfolders_checkbox_tooltip":"根据“按角色筛选”输入或帖子标题创建子文件夹。\n如果没有特定筛选器匹配，则使用“已知系列/角色”列表作为文件夹名称的后备。\n为单个帖子启用“按角色筛选”输入和“自定义文件夹名称”。",
"use_subfolder_per_post_checkbox_tooltip":"为每个帖子创建一个子文件夹。如果“分文件夹”也打开，则它位于角色/标题文件夹内。",
"use_cookie_checkbox_tooltip":"如果选中，将尝试使用应用程序目录中的“cookies.txt”（Netscape 格式）中的 cookie 进行请求。\n用于访问需要在 Kemono/Coomer 上登录的内容。",
"cookie_text_input_tooltip":"直接输入您的 cookie 字符串。\n如果选中了“使用 Cookie”并且“cookies.txt”未找到或此字段不为空，则将使用此字符串。\n格式取决于后端如何解析它（例如，“name1=value1; name2=value2”）。",
"use_multithreading_checkbox_tooltip":"启用并发操作。有关详细信息，请参见“线程数”输入。",
"thread_count_input_tooltip":"并发操作的数量。\n- 单个帖子：并发文件下载（建议 1-10 个）。\n- 创建者源 URL：要同时处理的帖子数量（建议 1-200 个）。\n每个帖子中的文件都由其工作线程逐个下载。\n如果未选中“使用多线程”，则使用 1 个线程。",
"external_links_checkbox_tooltip":"如果选中，主日志下方会出现一个辅助日志面板，以显示在帖子描述中找到的外部链接。\n（如果“仅链接”或“仅存档”模式处于活动状态，则禁用）。",
"manga_mode_checkbox_tooltip":"从最旧到最新下载帖子，并根据帖子标题重命名文件（仅限创建者源）。",
"multipart_on_button_text":"多部分：开",
"multipart_on_button_tooltip":"多部分下载：开\n\n启用同时以多个分段下载大文件。\n- 可以加快单个大文件（例如视频）的下载速度。\n- 可能会增加 CPU/网络使用率。\n- 对于有许多小文件的源，这可能不会带来速度优势，并且可能会使界面/日志变得繁忙。\n- 如果多部分下载失败，它会以单流方式重试。\n\n点击关闭。",
"multipart_off_button_text":"多部分：关",
"multipart_off_button_tooltip":"多部分下载：关\n\n所有文件都使用单流下载。\n- 稳定，适用于大多数情况，尤其是许多较小的文件。\n- 大文件按顺序下载。\n\n点击开启（请参阅建议）。",
"reset_button_text":"🔄 重置",
"reset_button_tooltip":"将所有输入和日志重置为默认状态（仅在空闲时）。",
"progress_idle_text":"进度：空闲",
"missed_character_log_label_text":"🚫 错过的角色日志：",
"creator_popup_title":"创作者选择",
"creator_popup_search_placeholder":"按名称、服务搜索或粘贴创作者 URL...",
"creator_popup_add_selected_button":"添加所选",
"creator_popup_scope_characters_button":"范围：角色",
"creator_popup_scope_creators_button":"范围：创作者",
"favorite_artists_button_text":"🖼️ 收藏的艺术家",
"favorite_artists_button_tooltip":"浏览并从您在 Kemono.su/Coomer.su 上收藏的艺术家那里下载。",
"favorite_posts_button_text":"📄 收藏的帖子",
"favorite_posts_button_tooltip":"浏览并下载您在 Kemono.su/Coomer.su 上收藏的帖子。",
"favorite_scope_selected_location_text":"范围：所选位置",
"favorite_scope_selected_location_tooltip":"当前收藏下载范围：所选位置\n\n所有选定的收藏艺术家/帖子都将下载到界面中指定的主“下载位置”。\n筛选器（角色、跳过词语、文件类型）将全局应用于所有内容。\n\n点击以更改为：艺术家文件夹",
"favorite_scope_artist_folders_text":"范围：艺术家文件夹",
"favorite_scope_artist_folders_tooltip":"当前收藏下载范围：艺术家文件夹\n\n对于每个选定的收藏艺术家/帖子，将在主“下载位置”内创建一个新的子文件夹（以艺术家命名）。\n该艺术家/帖子的内容将下载到其特定的子文件夹中。\n筛选器（角色、跳过词语、文件类型）将*在*每个艺术家的文件夹内应用。\n\n点击以更改为：所选位置",
"favorite_scope_unknown_text":"范围：未知",
"favorite_scope_unknown_tooltip":"收藏下载范围未知。点击以循环。",
"manga_style_post_title_text":"名称：帖子标题",
"manga_style_original_file_text":"名称：原始文件",
"manga_style_date_based_text":"名称：基于日期",
"manga_style_title_global_num_text":"名称：标题+全局编号",
"manga_style_unknown_text":"名称：未知样式",
"fav_artists_dialog_title":"收藏的艺术家",
"fav_artists_loading_status":"正在加载收藏的艺术家...",
"fav_artists_search_placeholder":"搜索艺术家...",
"fav_artists_select_all_button":"全选",
"fav_artists_deselect_all_button":"取消全选",
"fav_artists_download_selected_button":"下载所选",
"fav_artists_cancel_button":"取消",
"fav_artists_loading_from_source_status":"⏳ 正在从 {source_name} 加载收藏...",
"fav_artists_found_status":"总共找到 {count} 位收藏的艺术家。",
"fav_artists_none_found_status":"在 Kemono.su 或 Coomer.su 上未找到收藏的艺术家。",
"fav_artists_failed_status":"获取收藏失败。",
"fav_artists_cookies_required_status":"错误：已启用 Cookie，但无法为任何来源加载。",
"fav_artists_no_favorites_after_processing":"处理后未找到收藏的艺术家。",
"fav_artists_no_selection_title":"未选择",
"fav_artists_no_selection_message":"请至少选择一位要下载的艺术家。",
"fav_posts_dialog_title":"收藏的帖子",
"fav_posts_loading_status":"正在加载收藏的帖子...",
"fav_posts_search_placeholder":"搜索帖子（标题、创作者、ID、服务）...",
"fav_posts_select_all_button":"全选",
"fav_posts_deselect_all_button":"取消全选",
"fav_posts_download_selected_button":"下载所选",
"fav_posts_cancel_button":"取消",
"fav_posts_cookies_required_error":"错误：收藏的帖子需要 Cookie，但无法加载。",
"fav_posts_auth_failed_title":"授权失败（帖子）",
"fav_posts_auth_failed_message":"由于授权错误，无法获取收藏{domain_specific_part}：\n\n{error_message}\n\n这通常意味着您的 cookie 丢失、无效或已过期。请检查您的 cookie 设置。",
"fav_posts_fetch_error_title":"获取错误",
"fav_posts_fetch_error_message":"从 {domain}{error_message_part} 获取收藏时出错",
"fav_posts_no_posts_found_status":"未找到收藏的帖子。",
"fav_posts_found_status":"找到 {count} 个收藏的帖子。",
"fav_posts_display_error_status":"显示帖子时出错：{error}",
"fav_posts_ui_error_title":"界面错误",
"fav_posts_ui_error_message":"无法显示收藏的帖子：{error}",
"fav_posts_auth_failed_message_generic":"由于授权错误，无法获取收藏{domain_specific_part}。这通常意味着您的 cookie 丢失、无效或已过期。请检查您的 cookie 设置。",
"key_fetching_fav_post_list_init":"正在获取收藏的帖子列表...",
"key_fetching_from_source_kemono_su":"正在从 Kemono.su 获取收藏...",
"key_fetching_from_source_coomer_su":"正在从 Coomer.su 获取收藏...",
"fav_posts_fetch_cancelled_status":"收藏帖子获取已取消。",
"known_names_filter_dialog_title":"将已知名称添加到筛选器",
"known_names_filter_search_placeholder":"搜索名称...",
"known_names_filter_select_all_button":"全选",
"known_names_filter_deselect_all_button":"取消全选",
"known_names_filter_add_selected_button":"添加所选",
"error_files_dialog_title":"因错误而跳过的文件",
"error_files_no_errors_label":"在上次会话中或重试后，没有文件因错误而被记录为已跳过。",
"error_files_found_label":"由于下载错误，以下 {count} 个文件已被跳过：",
"error_files_select_all_button":"全选",
"error_files_retry_selected_button":"重试所选",
"error_files_export_urls_button":"将 URL 导出到 .txt",
"error_files_no_selection_retry_message":"请至少选择一个文件进行重试。",
"error_files_no_errors_export_title":"无错误",
"error_files_no_errors_export_message":"没有要导出的错误文件 URL。",
"error_files_no_urls_found_export_title":"未找到 URL",
"error_files_no_urls_found_export_message":"无法从错误文件列表中提取任何 URL 进行导出。",
"error_files_save_dialog_title":"保存错误文件 URL",
"error_files_export_success_title":"导出成功",
"error_files_export_success_message":"成功将 {count} 个条目导出到：\n{filepath}",
"error_files_export_error_title":"导出错误",
"error_files_export_error_message":"无法导出文件链接：{error}",
"export_options_dialog_title":"导出选项",
"export_options_description_label":"选择导出错误文件链接的格式：",
"export_options_radio_link_only":"每行一个链接（仅 URL）",
"export_options_radio_link_only_tooltip":"仅导出每个失败文件的直接下载 URL，每行一个 URL。",
"export_options_radio_with_details":"导出时附带详细信息（URL [帖子、文件信息]）",
"export_options_radio_with_details_tooltip":"导出 URL，后跟帖子标题、帖子 ID 和原始文件名等详细信息（在括号中）。",
"export_options_export_button":"导出",
"no_errors_logged_title":"未记录错误",
"no_errors_logged_message":"在上次会话中或重试后，没有文件因错误而被记录为已跳过。",
"progress_initializing_text":"进度：正在初始化...",
"progress_posts_text":"进度：{processed_posts} / {total_posts} 个帖子 ({progress_percent:.1f}%)",
"progress_processing_post_text":"进度：正在处理帖子 {processed_posts}...",
"progress_starting_text":"进度：正在开始...",
"downloading_file_known_size_text":"正在下载“{filename}”({downloaded_mb:.1f}MB / {total_mb:.1f}MB)",
"downloading_file_unknown_size_text":"正在下载“{filename}”({downloaded_mb:.1f}MB)",
"downloading_multipart_text":"下载“{filename}...”：{downloaded_mb:.1f}/{total_mb:.1f} MB（{parts} 个部分 @ {speed:.2f} MB/s）",
"downloading_multipart_initializing_text":"文件：{filename} - 正在初始化部分...",
"status_completed":"已完成",
"status_cancelled_by_user":"用户已取消",
"files_downloaded_label":"已下载",
"files_skipped_label":"已跳过",
"retry_finished_text":"重试完成",
"succeeded_text":"成功",
"failed_text":"失败",
"ready_for_new_task_text":"准备好执行新任务。",
"fav_mode_active_label_text":"⭐ 收藏模式已激活。请在选择您收藏的艺术家/帖子之前选择下面的筛选器。在下面选择操作。",
"export_links_button_text":"导出链接",
"download_extracted_links_button_text":"下载",
"download_selected_button_text":"下载所选",
"link_input_placeholder_text":"例如，https://kemono.su/patreon/user/12345 或 .../post/98765",
"link_input_tooltip_text":"输入 Kemono/Coomer 创建者页面或特定帖子的完整 URL。\n示例（创建者）：https://kemono.su/patreon/user/12345\n示例（帖子）：https://kemono.su/patreon/user/12345/post/98765",
"dir_input_placeholder_text":"选择将保存下载的文件夹",
"dir_input_tooltip_text":"输入或浏览到将保存所有下载内容的主文件夹。\n除非选择了“仅链接”模式，否则此字段是必需的。",
"character_input_placeholder_text":"例如，Tifa、Aerith、(Cloud, Zack)",
"custom_folder_input_placeholder_text":"可选：将此帖子保存到特定文件夹",
"custom_folder_input_tooltip_text":"如果下载单个帖子 URL 并且启用了“按名称/标题分文件夹”，\n您可以在此处为该帖子的下载文件夹输入自定义名称。\n示例：我最喜欢的场景",
"skip_words_input_placeholder_text":"例如，WM、WIP、sketch、preview",
"remove_from_filename_input_placeholder_text":"例如，patreon、HD",
"cookie_text_input_placeholder_no_file_selected_text":"Cookie 字符串（如果未选择 cookies.txt）",
"cookie_text_input_placeholder_with_file_selected_text":"正在使用所选的 cookie 文件（请参阅浏览...）",
"character_search_input_placeholder_text":"搜索角色...",
"character_search_input_tooltip_text":"在此处键入以筛选下面已知的系列/角色列表。",
"new_char_input_placeholder_text":"添加新的系列/角色名称",
"new_char_input_tooltip_text":"输入要添加到上面列表的新系列、游戏或角色名称。",
"link_search_input_placeholder_text":"搜索链接...",
"link_search_input_tooltip_text":"在“仅链接”模式下，在此处键入以按文本、URL 或平台筛选显示的链接。",
"manga_date_prefix_input_placeholder_text":"漫画文件名前缀",
"manga_date_prefix_input_tooltip_text":"“基于日期”或“原始文件”漫画文件名的可选前缀（例如，“系列名称”）。\n如果为空，文件将根据样式命名，不带前缀。",
"log_display_mode_links_view_text":"🔗 链接视图",
"log_display_mode_progress_view_text":"⬇️ 进度视图",
"download_external_links_dialog_title":"下载所选的外部链接",
"select_all_button_text":"全选",
"deselect_all_button_text":"取消全选",
"cookie_browse_button_tooltip":"浏览 cookie 文件（Netscape 格式，通常为 cookies.txt）。\n如果选中了“使用 Cookie”并且上面的文本字段为空，则将使用此文件。",
"page_range_label_text":"页面范围：",
"start_page_input_placeholder":"开始",
"start_page_input_tooltip":"对于创建者 URL：指定要从中下载的起始页码（例如，1、2、3）。\n留空或设置为 1 以从第一页开始。\n对于单个帖子 URL 或漫画/动漫模式禁用。",
"page_range_to_label_text":"到",
"end_page_input_placeholder":"结束",
"end_page_input_tooltip":"对于创建者 URL：指定要下载到的结束页码（例如，5、10）。\n留空以从起始页下载所有页面。\n对于单个帖子 URL 或漫画/动漫模式禁用。",
"known_names_help_button_tooltip_text":"打开应用程序功能指南。",
"future_settings_button_tooltip_text":"打开应用程序设置（主题、语言等）。",
"link_search_button_tooltip_text":"筛选显示的链接",
"confirm_add_all_dialog_title":"确认添加新名称",
"confirm_add_all_info_label":"您输入的“按角色筛选”中的以下新名称/组不在“Known.txt”中。\n添加它们可以改善将来下载的文件夹组织。\n\n请查看列表并选择一个操作：",
"confirm_add_all_select_all_button":"全选",
"confirm_add_all_deselect_all_button":"取消全选",
"confirm_add_all_add_selected_button":"将所选添加到 Known.txt",
"confirm_add_all_skip_adding_button":"跳过添加这些",
"confirm_add_all_cancel_download_button":"取消下载",
"cookie_help_dialog_title":"Cookie 文件说明",
"cookie_help_instruction_intro":"<p>要使用 cookie，您通常需要浏览器中的 <b>cookies.txt</b> 文件。</p>",
"cookie_help_how_to_get_title":"<p><b>如何获取 cookies.txt：</b></p>",
"cookie_help_step1_extension_intro":"<li>为您的基于 Chrome 的浏览器安装“Get cookies.txt LOCALLY”扩展程序：<br><a href=\"https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc\" style=\"color: #87CEEB;\">在 Chrome 网上应用店获取 Get cookies.txt LOCALLY</a></li>",
"cookie_help_step2_login":"<li>转到网站（例如，kemono.su 或 coomer.su）并根据需要登录。</li>",
"cookie_help_step3_click_icon":"<li>单击浏览器工具栏中的扩展程序图标。</li>",
"cookie_help_step4_export":"<li>单击“导出”按钮（例如，“导出为”、“导出 cookies.txt”——确切的措辞可能会因扩展程序版本而异）。</li>",
"cookie_help_step5_save_file":"<li>将下载的 <code>cookies.txt</code> 文件保存到您的计算机。</li>",
"cookie_help_step6_app_intro":"<li>在此应用程序中：<ul>",
"cookie_help_step6a_checkbox":"<li>确保选中“使用 Cookie”复选框。</li>",
"cookie_help_step6b_browse":"<li>单击 cookie 文本字段旁边的“浏览...”按钮。</li>",
"cookie_help_step6c_select":"<li>选择您刚刚保存的 <code>cookies.txt</code> 文件。</li></ul></li>",
"cookie_help_alternative_paste":"<p>或者，某些扩展程序可能允许您直接复制 cookie 字符串。如果是这样，您可以将其粘贴到文本字段中，而不是浏览文件。</p>",
"cookie_help_proceed_without_button":"不使用 Cookie 下载",
"empty_popup_button_tooltip_text": "打开创作者选择 (浏览 creators.json)",
"cookie_help_cancel_download_button":"取消下载",
"character_input_tooltip":"输入角色名称（以逗号分隔）。支持高级分组，并在启用“分文件夹”时影响文件夹命名。\n\n示例：\n- Nami → 匹配“Nami”，创建文件夹“Nami”。\n- (Ulti, Vivi) → 匹配任一者，文件夹“Ulti Vivi”，将两者分别添加到 Known.txt。\n- (Boa, Hancock)~ → 匹配任一者，文件夹“Boa Hancock”，在 Known.txt 中添加为一个组。\n\n名称被视为匹配的别名。\n\n筛选模式（按钮循环）：\n- 文件：按文件名筛选。\n- 标题：按帖子标题筛选。\n- 两者：标题优先，然后是文件名。\n- 评论（测试版）：文件名优先，然后是帖子评论。",
"tour_dialog_title":"欢迎使用 Kemono Downloader！",
"tour_dialog_never_show_checkbox":"不再显示此导览",
"tour_dialog_skip_button":"跳过导览",
"tour_dialog_back_button":"返回",
"tour_dialog_next_button":"下一步",
"tour_dialog_finish_button":"完成",
"tour_dialog_step1_title":"👋 欢迎！",
"tour_dialog_step1_content":"您好！此快速导览将带您了解 Kemono Downloader 的主要功能，包括最近的更新，如增强的筛选、漫画模式改进和 cookie 管理。\n<ul>\n<li>我的目标是帮助您轻松地从 <b>Kemono</b> 和 <b>Coomer</b> 下载内容。</li><br>\n<li><b>🎨 创建者选择按钮：</b>在 URL 输入旁边，单击调色板图标以打开一个对话框。浏览并从您的 <code>creators.json</code> 文件中选择创建者，以快速将其名称添加到 URL 输入中。</li><br>\n<li><b>重要提示：应用程序“（无响应）”？</b><br>\n单击“开始下载”后，尤其是在处理大型创建者源或使用许多线程时，应用程序可能会暂时显示为“（无响应）”。您的操作系统（Windows、macOS、Linux）甚至可能会建议您“结束进程”或“强制退出”。<br>\n<b>请耐心等待！</b>应用程序通常仍在后台努力工作。在强制关闭之前，请尝试在文件浏览器中检查您选择的“下载位置”。如果您看到正在创建新文件夹或出现文件，则表示下载正在正确进行。给它一些时间以再次响应。</li><br>\n<li>使用<b>下一步</b>和<b>返回</b>按钮进行导航。</li><br>\n<li>将鼠标悬停在许多选项上可以查看更多详细信息的工具提示。</li><br>\n<li>随时单击<b>跳过导览</b>以关闭本指南。</li><br>\n<li>如果您不希望在将来启动时看到此导览，请选中<b>“不再显示此导览”</b>。</li>\n</ul>",
"tour_dialog_step2_title":"① 入门",
"tour_dialog_step2_content":"让我们从下载的基础知识开始：\n<ul>\n<li><b>🔗 Kemono 创建者/帖子 URL：</b><br>\n粘贴创建者页面的完整网址（URL）（例如，<i>https://kemono.su/patreon/user/12345</i>）\n或特定帖子（例如，<i>.../post/98765</i>）。<br>\n或 Coomer 创建者（例如，<i>https://coomer.su/onlyfans/user/artistname</i>）</li><br>\n<li><b>📁 下载位置：</b><br>\n单击“浏览...”以选择计算机上的一个文件夹，所有下载的文件都将保存在该文件夹中。\n除非您使用“仅链接”模式，否则此字段是必需的。</li><br>\n<li><b>📄 页面范围（仅限创建者 URL）：</b><br>\n如果从创建者页面下载，您可以指定要获取的页面范围（例如，第 2 到 5 页）。\n留空以获取所有页面。对于单个帖子 URL 或当<b>漫画/动漫模式</b>处于活动状态时，此功能被禁用。</li>\n</ul>",
"tour_dialog_step3_title":"② 筛选下载",
"tour_dialog_step3_content":"使用这些筛选器优化您的下载（在“仅链接”或“仅存档”模式下，大多数筛选器都被禁用）：\n<ul>\n<li><b>🎯 按角色筛选：</b><br>\n输入角色名称，以逗号分隔（例如，<i>Tifa, Aerith</i>）。将别名分组以获得组合的文件夹名称：<i>(alias1, alias2, alias3)</i> 变为文件夹“alias1 alias2 alias3”（清理后）。组中的所有名称都用作匹配的别名。<br>\n此输入旁边的<b>“筛选：[类型]”</b>按钮可循环此筛选器的应用方式：\n<ul><li><i>筛选：文件：</i>检查单个文件名。如果任何文件匹配，则保留帖子；仅下载匹配的文件。文件夹命名使用匹配文件名中的角色（如果启用了“分文件夹”）。</li><br>\n<li><i>筛选：标题：</i>检查帖子标题。匹配帖子的所有文件都将被下载。文件夹命名使用匹配帖子标题中的角色。</li>\n<li><b>⤵️ 添加到筛选器按钮（已知名称）：</b>在已知名称的“添加”按钮旁边（参见第 5 步），这将打开一个弹出窗口。通过复选框（带搜索栏）从您的 <code>Known.txt</code> 列表中选择名称，以快速将其添加到“按角色筛选”字段。来自 Known.txt 的分组名称（如 <code>(Boa, Hancock)</code>）将作为 <code>(Boa, Hancock)~</code> 添加到筛选器中。</li><br>\n<li><i>筛选：两者：</i>首先检查帖子标题。如果匹配，则下载所有文件。如果不匹配，则检查文件名，并且仅下载匹配的文件。文件夹命名优先考虑标题匹配，然后是文件匹配。</li><br>\n<li><i>筛选：评论（测试版）：</i>首先检查文件名。如果文件匹配，则下载帖子中的所有文件。如果没有文件匹配，则检查帖子评论。如果评论匹配，则下载所有文件。（使用更多的 API 请求）。文件夹命名优先考虑文件匹配，然后是评论匹配。</li></ul>\n如果启用了“按名称/标题分文件夹”，此筛选器也会影响文件夹命名。</li><br>\n<li><b>🚫 使用关键词跳过：</b><br>\n输入词语，以逗号分隔（例如，<i>WIP, sketch, preview</i>）。\n此输入旁边的<b>“范围：[类型]”</b>按钮可循环此筛选器的应用方式：\n<ul><li><i>范围：文件：</i>如果文件名包含任何这些词语，则跳过文件。</li><br>\n<li><i>范围：帖子：</i>如果帖子标题包含任何这些词语，则跳过整个帖子。</li><br>\n<li><i>范围：两者：</i>同时应用文件和帖子标题跳过（帖子优先，然后是文件）。</li></ul></li><br>\n<li><b>筛选文件（单选按钮）：</b>选择要下载的内容：\n<ul>\n<li><i>全部：</i>下载找到的所有文件类型。</li><br>\n<li><i>图片/GIF：</i>仅常见的图像格式和 GIF。</li><br>\n<li><i>视频：</i>仅常见的视频格式。</li><br>\n<li><b><i>📦 仅存档：</i></b>专门下载 <b>.zip</b> 和 <b>.rar</b> 文件。选择此选项后，“跳过 .zip”和“跳过 .rar”复选框将自动禁用并取消选中。“显示外部链接”也将被禁用。</li><br>\n<li><i>🎧 仅音频：</i>仅常见的音频格式（MP3、WAV、FLAC 等）。</li><br>\n<li><i>🔗 仅链接：</i>从帖子描述中提取并显示外部链接，而不是下载文件。与下载相关的选项和“显示外部链接”将被禁用。</li>\n</ul></li>\n</ul>",
"tour_dialog_step4_title":"③ 收藏模式（替代下载）",
"tour_dialog_step4_content":"该应用程序提供“收藏模式”，用于从您在 Kemono.su 上收藏的艺术家那里下载内容。\n<ul>\n<li><b>⭐ 收藏模式复选框：</b><br>\n位于“🔗 仅链接”单选按钮旁边。选中此项以激活收藏模式。</li><br>\n<li><b>收藏模式下的情况：</b>\n<ul><li>“🔗 Kemono 创建者/帖子 URL”输入区域被一条消息替换，指示收藏模式已激活。</li><br>\n<li>标准的“开始下载”、“暂停”、“取消”按钮被替换为“🖼️ 收藏的艺术家”和“📄 收藏的帖子”按钮（注意：“收藏的帖子”计划在将来推出）。</li><br>\n<li>“🍪 使用 Cookie”选项被自动启用并锁定，因为获取您的收藏需要 cookie。</li></ul></li><br>\n<li><b>🖼️ 收藏的艺术家按钮：</b><br>\n单击此按钮可打开一个对话框，其中列出了您在 Kemono.su 上收藏的艺术家。您可以选择一个或多个艺术家进行下载。</li><br>\n<li><b>收藏下载范围（按钮）：</b><br>\n此按钮（在“收藏的帖子”旁边）控制所选收藏的下载位置：\n<ul><li><i>范围：所选位置：</i>所有选定的艺术家都下载到您设置的主“下载位置”。筛选器全局应用。</li><br>\n<li><i>范围：艺术家文件夹：</i>在您的主“下载位置”内为每个选定的艺术家创建一个子文件夹（以艺术家命名）。该艺术家的内容将进入其特定的子文件夹。筛选器在每个艺术家的文件夹内应用。</li></ul></li><br>\n<li><b>收藏模式下的筛选器：</b><br>\n“按角色筛选”、“使用关键词跳过”和“筛选文件”选项仍然适用于从您选定的收藏艺术家那里下载的内容。</li>\n</ul>",
"tour_dialog_step5_title":"④ 微调下载",
"tour_dialog_step5_content":"更多选项可自定义您的下载：\n<ul>\n<li><b>跳过 .zip / 跳过 .rar：</b>选中这些项以避免下载这些存档文件类型。\n<i>（注意：如果选择了“📦 仅存档”筛选模式，这些项将被禁用和忽略）。</i></li><br>\n<li><b>✂️ 从名称中删除词语：</b><br>\n输入词语，以逗号分隔（例如，<i>patreon, [HD]</i>），以从下载的文件名中删除（不区分大小写）。</li><br>\n<li><b>仅下载缩略图：</b>下载小预览图像，而不是全尺寸文件（如果可用）。</li><br>\n<li><b>压缩大图像：</b>如果安装了“Pillow”库，大于 1.5MB 的图像如果 WebP 版本明显更小，将被转换为 WebP 格式。</li><br>\n<li><b>🗄️ 自定义文件夹名称（仅限单个帖子）：</b><br>\n如果您正在下载单个特定帖子 URL 并且启用了“按名称/标题分文件夹”，\n您可以在此处为该帖子的下载文件夹输入自定义名称。</li><br>\n<li><b>🍪 使用 Cookie：</b>选中此项以使用 cookie 进行请求。您可以：\n<ul><li>直接在文本字段中输入 cookie 字符串（例如，<i>name1=value1; name2=value2</i>）。</li><br>\n<li>单击“浏览...”以选择一个 <i>cookies.txt</i> 文件（Netscape 格式）。路径将显示在文本字段中。</li></ul>\n这对于访问需要登录的内容很有用。如果填写，文本字段优先。\n如果选中了“使用 Cookie”，但文本字段和浏览的文件都为空，它将尝试从应用程序的目录加载“cookies.txt”。</li>\n</ul>",
"tour_dialog_step6_title":"⑤ 组织与性能",
"tour_dialog_step6_content":"组织您的下载并管理性能：\n<ul>\n<li><b>⚙️ 按名称/标题分文件夹：</b>根据“按角色筛选”输入或帖子标题创建子文件夹（如果帖子与您的活动“按角色筛选”输入不匹配，可以使用 <b>Known.txt</b> 列表作为后备）。</li><br>\n<li><b>每篇帖子一个子文件夹：</b>如果“分文件夹”打开，这将在主角色/标题文件夹内为<i>每篇单独的帖子</i>创建一个额外的子文件夹。</li><br>\n<li><b>🚀 使用多线程（线程数）：</b>启用更快的操作。“线程数”输入中的数字表示：\n<ul><li>对于<b>创建者源：</b>要同时处理的帖子数量。每个帖子中的文件都由其工作线程按顺序下载（除非启用了“基于日期”的漫画命名，这会强制使用 1 个帖子工作线程）。</li><br>\n<li>对于<b>单个帖子 URL：</b>要从该单个帖子同时下载的文件数量。</li></ul>\n如果未选中，则使用 1 个线程。高线程数（例如 >40）可能会显示建议。</li><br>\n<li><b>多部分下载切换（日志区域右上角）：</b><br>\n<b>“多部分：[开/关]”</b>按钮允许为单个大文件启用/禁用多段下载。\n<ul><li><b>开：</b>可以加快大文件的下载速度（例如视频），但可能会增加界面的卡顿或在有许多小文件时产生日志垃圾信息。启用时会出现建议。如果多部分下载失败，它会以单流方式重试。</li><br>\n<li><b>关（默认）：</b>文件以单流方式下载。</li></ul>\n如果“仅链接”或“仅存档”模式处于活动状态，此功能将被禁用。</li><br>\n<li><b>📖 漫画/动漫模式（仅限创建者 URL）：</b>专为顺序内容量身定制。\n<ul>\n<li>从<b>最旧到最新</b>下载帖子。</li><br>\n<li>“页面范围”输入被禁用，因为所有帖子都将被获取。</li><br>\n<li>当此模式对创建者源处于活动状态时，日志区域的右上角会出现一个<b>文件名样式切换按钮</b>（例如，“名称：帖子标题”）。单击它以在命名样式之间循环：\n<ul>\n<li><b><i>名称：帖子标题（默认）：</i></b>帖子中的第一个文件以帖子的清理标题命名（例如，“我的第一章.jpg”）。*同一帖子*中的后续文件将尝试保留其原始文件名（例如，“page_02.png”、“bonus_art.jpg”）。如果帖子只有一个文件，则以帖子标题命名。这通常是大多数漫画/动漫的推荐设置。</li><br>\n<li><b><i>名称：原始文件：</i></b>所有文件都尝试保留其原始文件名。可以在样式按钮旁边出现的输入字段中输入可选的前缀（例如，“我的系列_”）。示例：“我的系列_原始文件.jpg”。</li><br>\n<li><b><i>名称：标题+全局编号（帖子标题 + 全局编号）：</i></b>当前下载会话中所有帖子的所有文件都使用帖子的清理标题作为前缀，后跟一个全局计数器，按顺序命名。例如：帖子“第一章”（2 个文件）->“第一章_001.jpg”、“第一章_002.png”。下一个帖子“第二章”（1 个文件）将继续编号 ->“第二章_003.jpg”。为了确保正确的全局编号，此样式的帖子处理多线程被自动禁用。</li><br>\n<li><b><i>名称：基于日期：</i></b>文件根据帖子发布顺序按顺序命名（001.ext、002.ext ...）。可以在样式按钮旁边出现的输入字段中输入可选的前缀（例如，“我的系列_”）。示例：“我的系列_001.jpg”。此样式的帖子处理多线程被自动禁用。</li>\n</ul>\n</li><br>\n<li>为了在使用“名称：帖子标题”、“名称：标题+全局编号”或“名称：基于日期”样式时获得最佳效果，请使用“按角色筛选”字段以及漫画/系列标题进行文件夹组织。</li>\n</ul></li><br>\n<li><b>🎭 Known.txt 用于智能文件夹组织：</b><br>\n<code>Known.txt</code>（在应用程序的目录中）允许在启用“按名称/标题分文件夹”时对自动文件夹组织进行精细控制。\n<ul>\n<li><b>工作原理：</b><code>Known.txt</code> 中的每一行都是一个条目。\n<ul><li>像 <code>我的精彩系列</code> 这样的简单行意味着匹配此内容的内容将进入名为“我的精彩系列”的文件夹。</li><br>\n<li>像 <code>(角色 A, 角色 A, 备用名 A)</code> 这样的分组行意味着匹配“角色 A”、“角色 A”或“备用名 A”的内容将全部进入一个名为“角色 A 角色 A 备用名 A”的文件夹（清理后）。括号中的所有术语都成为该文件夹的别名。</li></ul></li>\n<li><b>智能后备：</b>当“按名称/标题分文件夹”处于活动状态，并且帖子与任何特定的“按角色筛选”输入不匹配时，下载器会查阅 <code>Known.txt</code> 以查找匹配的主名称以创建文件夹。</li><br>\n<li><b>用户友好的管理：</b>通过下面的 UI 列表添加简单（非分组）的名称。对于高级编辑（如创建/修改分组别名），请单击<b>“打开 Known.txt”</b>以在文本编辑器中编辑文件。应用程序会在下次使用或启动时重新加载它。</li>\n</ul>\n</li>\n</ul>",
"tour_dialog_step7_title":"⑥ 常见错误与故障排除",
"tour_dialog_step7_content":"有时，下载可能会遇到问题。以下是一些常见问题：\n<ul>\n<li><b>角色输入工具提示：</b><br>\n输入角色名称，以逗号分隔（例如，<i>Tifa, Aerith</i>）。<br>\n将别名分组以获得组合的文件夹名称：<i>(alias1, alias2, alias3)</i> 变为文件夹“alias1 alias2 alias3”。<br>\n组中的所有名称都用作匹配内容的别名。<br><br>\n此输入旁边的“筛选：[类型]”按钮可循环此筛选器的应用方式：<br>\n- 筛选：文件：检查单个文件名。仅下载匹配的文件。<br>\n- 筛选：标题：检查帖子标题。匹配帖子的所有文件都将被下载。<br>\n- 筛选：两者：首先检查帖子标题。如果不匹配，则检查文件名。<br>\n- 筛选：评论（测试版）：首先检查文件名。如果不匹配，则检查帖子评论。<br><br>\n如果启用了“按名称/标题分文件夹”，此筛选器也会影响文件夹命名。</li><br>\n<li><b>502 Bad Gateway / 503 Service Unavailable / 504 Gateway Timeout：</b><br>\n这些通常表示 Kemono/Coomer 存在临时服务器端问题。网站可能超载、停机维护或遇到问题。<br>\n<b>解决方法：</b>稍等片刻（例如，30 分钟到几个小时），然后重试。直接在浏览器中检查网站。</li><br>\n<li><b>连接丢失/连接被拒绝/超时（文件下载期间）：</b><br>\n这可能是由于您的互联网连接、服务器不稳定或服务器断开大文件连接所致。<br>\n<b>解决方法：</b>检查您的互联网。如果“线程数”很高，请尝试减少它。应用程序可能会在会话结束时提示重试某些失败的文件。</li><br>\n<li><b>IncompleteRead 错误：</b><br>\n服务器发送的数据少于预期。通常是暂时的网络故障或服务器问题。<br>\n<b>解决方法：</b>应用程序通常会将这些文件标记为在下载会话结束时重试。</li><br>\n<li><b>403 Forbidden / 401 Unauthorized（对于公共帖子不太常见）：</b><br>\n您可能没有访问内容的权限。对于某些付费或私人内容，使用“使用 Cookie”选项以及来自浏览器会话的有效 cookie 可能会有所帮助。请确保您的 cookie 是最新的。</li><br>\n<li><b>404 Not Found：</b><br>\n帖子或文件 URL 不正确，或者内容已从网站上删除。请仔细检查 URL。</li><br>\n<li><b>“未找到帖子”/“未找到目标帖子”：</b><br>\n确保 URL 正确，并且创建者/帖子存在。如果使用页面范围，请确保它们对创建者有效。对于非常新的帖子，API 中可能会有轻微延迟。</li><br>\n<li><b>普遍缓慢/应用程序“（无响应）”：</b><br>\n如第 1 步所述，如果应用程序在启动后似乎挂起，尤其是在处理大型创建者源或使用许多线程时，请给它一些时间。它很可能正在后台处理数据。如果这种情况频繁发生，减少线程数有时可以提高响应能力。</li>\n</ul>",
"tour_dialog_step8_title":"⑦ 日志与最终控件",
"tour_dialog_step8_content":"监控与控件：\n<ul>\n<li><b>📜 进度日志/提取的链接日志：</b>显示详细的下载消息。如果“🔗 仅链接”模式处于活动状态，此区域将显示提取的链接。</li><br>\n<li><b>在日志中显示外部链接：</b>如果选中，主日志下方会出现一个辅助日志面板，以显示在帖子描述中找到的任何外部链接。<i>（如果“🔗 仅链接”或“📦 仅存档”模式处于活动状态，则禁用）。</i></li><br>\n<li><b>日志视图切换（👁️ / 🙈 按钮）：</b><br>\n此按钮（日志区域右上角）可切换主日志视图：\n<ul><li><b>👁️ 进度日志（默认）：</b>显示所有下载活动、错误和摘要。</li><br>\n<li><b>🙈 错过的角色日志：</b>显示由于您的“按角色筛选”设置而跳过的帖子标题中的关键词列表。用于识别您可能无意中错过的内容。</li></ul></li><br>\n<li><b>🔄 重置：</b>清除所有输入字段、日志，并将临时设置重置为默认值。仅在没有下载活动时才能使用。</li><br>\n<li><b>⬇️ 开始下载/🔗 提取链接/⏸️ 暂停/❌ 取消：</b>这些按钮控制过程。“取消并重置界面”会停止当前操作并执行软界面重置，保留您的 URL 和目录输入。“暂停/继续”允许临时停止和继续。</li><br>\n<li>如果某些文件因可恢复的错误（如“IncompleteRead”）而失败，您可能会在会话结束时被提示重试它们。</li>\n</ul>\n<br>一切就绪！单击<b>“完成”</b>关闭导览并开始使用下载器。",
"help_guide_dialog_title":"Kemono Downloader - 功能指南",
"help_guide_github_tooltip":"访问项目的 GitHub 页面（在浏览器中打开）",
"help_guide_instagram_tooltip":"访问我们的 Instagram 页面（在浏览器中打开）",
"help_guide_discord_tooltip":"访问我们的 Discord 社区（在浏览器中打开）",
"help_guide_step1_title":"① 简介与主要输入",
"help_guide_step1_content":"<html><head/><body>\n<p>本指南概述了 Kemono Downloader 的功能、字段和按钮。</p>\n<h3>主要输入区（左上角）</h3>\n<ul>\n<li><b>🔗 Kemono 创建者/帖子 URL：</b>\n<ul>\n<li>输入创建者页面的完整网址（例如，<i>https://kemono.su/patreon/user/12345</i>）或特定帖子（例如，<i>.../post/98765</i>）。</li>\n<li>支持 Kemono (kemono.su, kemono.party) 和 Coomer (coomer.su, coomer.party) 的 URL。</li>\n</ul>\n</li>\n<li><b>页面范围（开始到结束）：</b>\n<ul>\n<li>对于创建者 URL：指定要获取的页面范围（例如，第 2 到 5 页）。留空以获取所有页面。</li>\n<li>对于单个帖子 URL 或当<b>漫画/动漫模式</b>处于活动状态时禁用。</li>\n</ul>\n</li>\n<li><b>📁 下载位置：</b>\n<ul>\n<li>单击<b>“浏览...”</b>以选择计算机上的一个主文件夹，所有下载的文件都将保存在该文件夹中。</li>\n<li>除非您使用<b>“🔗 仅链接”</b>模式，否则此字段是必需的。</li>\n</ul>\n</li>\n<li><b>🎨 创建者选择按钮（URL 输入旁边）：</b>\n<ul>\n<li>单击调色板图标（🎨）以打开“创建者选择”对话框。</li>\n<li>此对话框从您的 <code>creators.json</code> 文件（应位于应用程序的目录中）加载创建者。</li>\n<li><b>对话框内部：</b>\n<ul>\n<li><b>搜索栏：</b>键入以按名称或服务筛选创建者列表。</li>\n<li><b>创建者列表：</b>显示来自您的 <code>creators.json</code> 的创建者。您已“收藏”的创建者（在 JSON 数据中）显示在顶部。</li>\n<li><b>复选框：</b>通过选中其名称旁边的框来选择一个或多个创建者。</li>\n<li><b>“范围”按钮（例如，“范围：角色”）：</b>此按钮在从此弹出窗口启动下载时切换下载组织：\n<ul><li><i>范围：角色：</i>下载将直接组织到您主“下载位置”中以角色命名的文件夹中。来自不同创建者的同一角色的艺术作品将被分组在一起。</li>\n<li><i>范围：创建者：</i>下载将首先在您的主“下载位置”内创建一个以创建者命名的文件夹。然后，以角色命名的子文件夹将创建在每个创建者的文件夹内。</li></ul>\n</li>\n<li><b>“添加所选”按钮：</b>单击此按钮将获取所有选定创建者的名称，并将其以逗号分隔的方式添加到主“🔗 Kemono 创建者/帖子 URL”输入字段中。然后对话框将关闭。</li>\n</ul>\n</li>\n<li>此功能提供了一种快速填充多个创建者 URL 字段的方法，而无需手动键入或粘贴每个 URL。</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step2_title":"② 筛选下载",
"help_guide_step2_content":"<html><head/><body>\n<h3>筛选下载（左侧面板）</h3>\n<ul>\n<li><b>🎯 按角色筛选：</b>\n<ul>\n<li>输入名称，以逗号分隔（例如，<code>Tifa, Aerith</code>）。</li>\n<li><b>用于共享文件夹的分组别名（单独的 Known.txt 条目）：</b><code>(Vivi, Ulti, Uta)</code>。\n<ul><li>匹配“Vivi”、“Ulti”或“Uta”的内容将进入名为“Vivi Ulti Uta”的共享文件夹（清理后）。</li>\n<li>如果这些名称是新的，系统将提示将“Vivi”、“Ulti”和“Uta”作为<i>单独的单个条目</i>添加到 <code>Known.txt</code>。</li>\n</ul>\n</li>\n<li><b>用于共享文件夹的分组别名（单个 Known.txt 条目）：</b><code>(Yuffie, Sonon)~</code>（注意波浪号 <code>~</code>）。\n<ul><li>匹配“Yuffie”或“Sonon”的内容将进入名为“Yuffie Sonon”的共享文件夹。</li>\n<li>如果是新的，“Yuffie Sonon”（别名为 Yuffie, Sonon）将被提示作为<i>单个组条目</i>添加到 <code>Known.txt</code>。</li>\n</ul>\n</li>\n<li>如果启用了“按名称/标题分文件夹”，此筛选器会影响文件夹命名。</li>\n</ul>\n</li>\n<li><b>筛选：[类型] 按钮（角色筛选范围）：</b>循环“按角色筛选”的应用方式：\n<ul>\n<li><code>筛选：文件</code>：检查单个文件名。如果任何文件匹配，则保留帖子；仅下载匹配的文件。文件夹命名使用匹配文件名中的角色。</li>\n<li><code>筛选：标题</code>：检查帖子标题。匹配帖子的所有文件都将被下载。文件夹命名使用匹配帖子标题中的角色。</li>\n<li><code>筛选：两者</code>：首先检查帖子标题。如果匹配，则下载所有文件。如果不匹配，则检查文件名，并且仅下载匹配的文件。文件夹命名优先考虑标题匹配，然后是文件匹配。</li>\n<li><code>筛选：评论（测试版）</code>：首先检查文件名。如果文件匹配，则下载帖子中的所有文件。如果没有文件匹配，则检查帖子评论。如果评论匹配，则下载所有文件。（使用更多的 API 请求）。文件夹命名优先考虑文件匹配，然后是评论匹配。</li>\n</ul>\n</li>\n<li><b>🗄️ 自定义文件夹名称（仅限单个帖子）：</b>\n<ul>\n<li>仅在下载单个特定帖子 URL 并且启用了“按名称/标题分文件夹”时可见和可用。</li>\n<li>允许您为该单个帖子的下载文件夹指定自定义名称。</li>\n</ul>\n</li>\n<li><b>🚫 使用关键词跳过：</b>\n<ul><li>输入词语，以逗号分隔（例如，<code>WIP, sketch, preview</code>）以跳过某些内容。</li></ul>\n</li>\n<li><b>范围：[类型] 按钮（跳过词语范围）：</b>循环“使用关键词跳过”的应用方式：\n<ul>\n<li><code>范围：文件</code>：如果文件名包含任何这些词语，则跳过单个文件。</li>\n<li><code>范围：帖子</code>：如果帖子标题包含任何这些词语，则跳过整个帖子。</li>\n<li><code>范围：两者</code>：同时应用两者（帖子标题优先，然后是单个文件）。</li>\n</ul>\n</li>\n<li><b>✂️ 从名称中删除词语：</b>\n<ul><li>输入词语，以逗号分隔（例如，<code>patreon, [HD]</code>），以从下载的文件名中删除（不区分大小写）。</li></ul>\n</li>\n<li><b>筛选文件（单选按钮）：</b>选择要下载的内容：\n<ul>\n<li><code>全部</code>：下载找到的所有文件类型。</li>\n<li><code>图片/GIF</code>：仅常见的图像格式（JPG、PNG、GIF、WEBP 等）和 GIF。</li>\n<li><code>视频</code>：仅常见的视频格式（MP4、MKV、WEBM、MOV 等）。</li>\n<li><code>📦 仅存档</code>：专门下载 <b>.zip</b> 和 <b>.rar</b> 文件。选择此选项后，“跳过 .zip”和“跳过 .rar”复选框将自动禁用并取消选中。“显示外部链接”也将被禁用。</li>\n<li><code>🎧 仅音频</code>：仅下载常见的音频格式（MP3、WAV、FLAC、M4A、OGG 等）。其他特定于文件的选项的行为与“图片”或“视频”模式相同。</li>\n<li><code>🔗 仅链接</code>：从帖子描述中提取并显示外部链接，而不是下载文件。与下载相关的选项和“显示外部链接”将被禁用。主下载按钮变为“🔗 提取链接”。</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step3_title":"③ 下载选项与设置",
"help_guide_step3_content":"<html><head/><body>\n<h3>下载选项与设置（左侧面板）</h3>\n<ul>\n<li><b>跳过 .zip / 跳过 .rar：</b>用于避免下载这些存档文件类型的复选框。（如果选择了“📦 仅存档”筛选模式，则禁用和忽略）。</li>\n<li><b>仅下载缩略图：</b>下载小预览图像，而不是全尺寸文件（如果可用）。</li>\n<li><b>压缩大图像（为 WebP）：</b>如果安装了“Pillow”（PIL）库，大于 1.5MB 的图像如果 WebP 版本明显更小，将被转换为 WebP 格式。</li>\n<li><b>⚙️ 高级设置：</b>\n<ul>\n<li><b>按名称/标题分文件夹：</b>根据“按角色筛选”输入或帖子标题创建子文件夹。可以使用 <b>Known.txt</b> 列表作为文件夹名称的后备。</li></ul></li></ul></body></html>",
"help_guide_step4_title":"④ 高级设置（第 1 部分）",
"help_guide_step4_content":"<html><head/><body><h3>⚙️ 高级设置（续）</h3><ul><ul>\n<li><b>每篇帖子一个子文件夹：</b>如果“分文件夹”打开，这将在主角色/标题文件夹内为<i>每篇单独的帖子</i>创建一个额外的子文件夹。</li>\n<li><b>使用 Cookie：</b>选中此项以使用 cookie 进行请求。\n<ul>\n<li><b>文本字段：</b>直接输入 cookie 字符串（例如，<code>name1=value1; name2=value2</code>）。</li>\n<li><b>浏览...：</b>选择一个 <code>cookies.txt</code> 文件（Netscape 格式）。路径将显示在文本字段中。</li>\n<li><b>优先级：</b>文本字段（如果填写）优先于浏览的文件。如果选中了“使用 Cookie”，但两者都为空，它将尝试从应用程序的目录加载 <code>cookies.txt</code>。</li>\n</ul>\n</li>\n<li><b>使用多线程和线程数输入：</b>\n<ul>\n<li>启用更快的操作。“线程数”输入中的数字表示：\n<ul>\n<li>对于<b>创建者源：</b>要同时处理的帖子数量。每个帖子中的文件都由其工作线程按顺序下载（除非启用了“基于日期”的漫画命名，这会强制使用 1 个帖子工作线程）。</li>\n<li>对于<b>单个帖子 URL：</b>要从该单个帖子同时下载的文件数量。</li>\n</ul>\n</li>\n<li>如果未选中，则使用 1 个线程。高线程数（例如 >40）可能会显示建议。</li>\n</ul>\n</li></ul></ul></body></html>",
"help_guide_step5_title":"⑤ 高级设置（第 2 部分）与操作",
"help_guide_step5_content":"<html><head/><body><h3>⚙️ 高级设置（续）</h3><ul><ul>\n<li><b>在日志中显示外部链接：</b>如果选中，主日志下方会出现一个辅助日志面板，以显示在帖子描述中找到的任何外部链接。（如果“🔗 仅链接”或“📦 仅存档”模式处于活动状态，则禁用）。</li>\n<li><b>📖 漫画/动漫模式（仅限创建者 URL）：</b>专为顺序内容量身定制。\n<ul>\n<li>从<b>最旧到最新</b>下载帖子。</li>\n<li>“页面范围”输入被禁用，因为所有帖子都将被获取。</li>\n<li>当此模式对创建者源处于活动状态时，日志区域的右上角会出现一个<b>文件名样式切换按钮</b>（例如，“名称：帖子标题”）。单击它以在命名样式之间循环：\n<ul>\n<li><code>名称：帖子标题（默认）</code>：帖子中的第一个文件以帖子的清理标题命名（例如，“我的第一章.jpg”）。*同一帖子*中的后续文件将尝试保留其原始文件名（例如，“page_02.png”、“bonus_art.jpg”）。如果帖子只有一个文件，则以帖子标题命名。这通常是大多数漫画/动漫的推荐设置。</li>\n<li><code>名称：原始文件</code>：所有文件都尝试保留其原始文件名。</li>\n<li><code>名称：原始文件</code>：所有文件都尝试保留其原始文件名。当此样式处于活动状态时，样式按钮旁边会出现一个用于<b>可选文件名前缀</b>的输入字段（例如，“我的系列_”）。示例：“我的系列_原始文件.jpg”。</li>\n<li><code>名称：标题+全局编号（帖子标题 + 全局编号）</code>：当前下载会话中所有帖子的所有文件都使用帖子的清理标题作为前缀，后跟一个全局计数器，按顺序命名。示例：帖子“第一章”（2 个文件）->“第一章 001.jpg”、“第一章 002.png”。下一个帖子“第二章”（1 个文件）->“第二章 003.jpg”。为了确保正确的全局编号，此样式的帖子处理多线程被自动禁用。</li>\n<li><code>名称：基于日期</code>：文件根据帖子发布顺序按顺序命名（001.ext、002.ext ...）。当此样式处于活动状态时，样式按钮旁边会出现一个用于<b>可选文件名前缀</b>的输入字段（例如，“我的系列_”）。示例：“我的系列_001.jpg”。此样式的帖子处理多线程被自动禁用。</li>\n</ul>\n</li>\n<li>为了在使用“名称：帖子标题”、“名称：标题+全局编号”或“名称：基于日期”样式时获得最佳效果，请使用“按角色筛选”字段以及漫画/系列标题进行文件夹组织。</li>\n</ul>\n</li>\n</ul></li></ul>\n<h3>主要操作按钮（左侧面板）</h3>\n<ul>\n<li><b>⬇️ 开始下载/🔗 提取链接：</b>此按钮的文本和功能根据“筛选文件”单选按钮的选择而变化。它启动主要操作。</li>\n<li><b>⏸️ 暂停下载/▶️ 继续下载：</b>允许您临时停止当前下载/提取过程并稍后继续。暂停时可以更改某些界面设置。</li>\n<li><b>❌ 取消并重置界面：</b>停止当前操作并执行软界面重置。您的 URL 和下载目录输入将被保留，但其他设置和日志将被清除。</li>\n</ul></body></html>",
"help_guide_step6_title":"⑥ 已知系列/角色列表",
"help_guide_step6_content":"<html><head/><body>\n<h3>已知系列/角色列表管理（左下角）</h3>\n<p>本节帮助管理 <code>Known.txt</code> 文件，该文件用于在启用“按名称/标题分文件夹”时进行智能文件夹组织，尤其是在帖子与您的活动“按角色筛选”输入不匹配时作为后备。</p>\n<ul>\n<li><b>打开 Known.txt：</b>在您的默认文本编辑器中打开 <code>Known.txt</code> 文件（位于应用程序的目录中），以进行高级编辑（如创建复杂的分组别名）。</li>\n<li><b>搜索角色...：</b>筛选下面显示的已知名称列表。</li>\n<li><b>列表小部件：</b>显示来自您的 <code>Known.txt</code> 的主名称。在此处选择条目以将其删除。</li>\n<li><b>添加新的系列/角色名称（输入字段）：</b>输入要添加的名称或组。\n<ul>\n<li><b>简单名称：</b>例如，<code>我的精彩系列</code>。作为单个条目添加。</li>\n<li><b>用于单独的 Known.txt 条目的组：</b>例如，<code>(Vivi, Ulti, Uta)</code>。将“Vivi”、“Ulti”和“Uta”作为三个单独的单个条目添加到 <code>Known.txt</code>。</li>\n<li><b>用于共享文件夹和单个 Known.txt 条目的组（波浪号 <code>~</code>）：</b>例如，<code>(角色 A, 角色 A)~</code>。在 <code>Known.txt</code> 中添加一个名为“角色 A 角色 A”的条目。“角色 A”和“角色 A”成为此单个文件夹/条目的别名。</li>\n</ul>\n</li>\n<li><b>➕ 添加按钮：</b>将上面输入字段中的名称/组添加到列表和 <code>Known.txt</code>。</li>\n<li><b>⤵️ 添加到筛选器按钮：</b>\n<ul>\n<li>位于“已知系列/角色”列表的“➕ 添加”按钮旁边。</li>\n<li>单击此按钮将打开一个弹出窗口，其中显示来自您的 <code>Known.txt</code> 文件的所有名称，每个名称都有一个复选框。</li>\n<li>该弹出窗口包括一个搜索栏，可快速筛选名称列表。</li>\n<li>您可以使用复选框选择一个或多个名称。</li>\n<li>单击“添加所选”以将所选名称插入主窗口中的“按角色筛选”输入字段。</li>\n<li>如果从 <code>Known.txt</code> 中选择的名称最初是一个组（例如，在 Known.txt 中定义为 <code>(Boa, Hancock)</code>），它将被添加为 <code>(Boa, Hancock)~</code> 到筛选字段。简单名称按原样添加。</li>\n<li>为了方便起见，弹出窗口中提供了“全选”和“取消全选”按钮。</li>\n<li>单击“取消”以关闭弹出窗口而不进行任何更改。</li>\n</ul>\n</li>\n<li><b>🗑️ 删除所选按钮：</b>从列表和 <code>Known.txt</code> 中删除所选的名称。</li>\n<li><b>❓ 按钮（就是这个！）：</b>显示此综合帮助指南。</li>\n</ul></body></html>",
"help_guide_step7_title":"⑦ 日志区与控件",
"help_guide_step7_content":"<html><head/><body>\n<h3>日志区与控件（右侧面板）</h3>\n<ul>\n<li><b>📜 进度日志/提取的链接日志（标签）：</b>主日志区的标题；如果“🔗 仅链接”模式处于活动状态，则会更改。</li>\n<li><b>搜索链接... / 🔍 按钮（链接搜索）：</b>\n<ul><li>仅在“🔗 仅链接”模式处于活动状态时可见。允许按文本、URL 或平台实时筛选主日志中显示的提取链接。</li></ul>\n</li>\n<li><b>名称：[样式] 按钮（漫画文件名样式）：</b>\n<ul><li>仅在<b>漫画/动漫模式</b>对创建者源处于活动状态且不在“仅链接”或“仅存档”模式时可见。</li>\n<li>在文件名样式之间循环：<code>帖子标题</code>、<code>原始文件</code>、<code>基于日期</code>。（有关详细信息，请参阅漫画/动漫模式部分）。</li>\n<li>当“原始文件”或“基于日期”样式处于活动状态时，此按钮旁边会出现一个用于<b>可选文件名前缀</b>的输入字段。</li>\n</ul>\n</li>\n<li><b>多部分：[开/关] 按钮：</b>\n<ul><li>切换单个大文件的多段下载。\n<ul><li><b>开：</b>可以加快大文件的下载速度（例如视频），但可能会增加界面的卡顿或在有许多小文件时产生日志垃圾信息。启用时会出现建议。如果多部分下载失败，它会以单流方式重试。</li>\n<li><b>关（默认）：</b>文件以单流方式下载。</li>\n</ul>\n<li>如果“🔗 仅链接”或“📦 仅存档”模式处于活动状态，则禁用。</li>\n</ul>\n</li>\n<li><b>👁️ / 🙈 按钮（日志视图切换）：</b>切换主日志视图：\n<ul>\n<li><b>👁️ 进度日志（默认）：</b>显示所有下载活动、错误和摘要。</li>\n<li><b>🙈 错过的角色日志：</b>显示由于您的“按角色筛选”设置而跳过的帖子标题/内容中的关键词列表。用于识别您可能无意中错过的内容。</li>\n</ul>\n</li>\n<li><b>🔄 重置按钮：</b>清除所有输入字段、日志，并将临时设置重置为默认值。仅在没有下载活动时才能使用。</li>\n<li><b>主日志输出（文本区）：</b>显示详细的进度消息、错误和摘要。如果“🔗 仅链接”模式处于活动状态，此区域将显示提取的链接。</li>\n<li><b>错过的角色日志输出（文本区）：</b>（可通过 👁️ / 🙈 切换查看）显示由于角色筛选器而跳过的帖子/文件。</li>\n<li><b>外部日志输出（文本区）：</b>如果选中“在日志中显示外部链接”，则显示在主日志下方。显示在帖子描述中找到的外部链接。</li>\n<li><b>导出链接按钮：</b>\n<ul><li>仅在“🔗 仅链接”模式处于活动状态且已提取链接时可见和启用。</li>\n<li>允许您将所有提取的链接保存到 <code>.txt</code> 文件。</li>\n</ul>\n</li>\n<li><b>进度：[状态] 标签：</b>显示下载或链接提取过程的总体进度（例如，已处理的帖子）。</li>\n<li><b>文件进度标签：</b>显示单个文件下载的进度，包括速度和大小，或多部分下载状态。</li>\n</ul></body></html>",
"help_guide_step8_title":"⑧ 收藏模式与未来功能",
"help_guide_step8_content":"<html><head/><body>\n<h3>收藏模式（从您的 Kemono.su 收藏中下载）</h3>\n<p>此模式允许您直接从您在 Kemono.su 上收藏的艺术家那里下载内容。</p>\n<ul>\n<li><b>⭐ 如何启用：</b>\n<ul>\n<li>选中位于“🔗 仅链接”单选按钮旁边的<b>“⭐ 收藏模式”</b>复选框。</li>\n</ul>\n</li>\n<li><b>收藏模式下的界面更改：</b>\n<ul>\n<li>“🔗 Kemono 创建者/帖子 URL”输入区域被一条消息替换，指示收藏模式已激活。</li>\n<li>标准的“开始下载”、“暂停”、“取消”按钮被替换为：\n<ul>\n<li><b>“🖼️ 收藏的艺术家”</b>按钮</li>\n<li><b>“📄 收藏的帖子”</b>按钮</li>\n</ul>\n</li>\n<li>“🍪 使用 Cookie”选项被自动启用并锁定，因为获取您的收藏需要 cookie。</li>\n</ul>\n</li>\n<li><b>🖼️ 收藏的艺术家按钮：</b>\n<ul>\n<li>单击此按钮将打开一个对话框，其中列出了您在 Kemono.su 上收藏的所有艺术家。</li>\n<li>您可以从此列表中选择一个或多个艺术家以下载其内容。</li>\n</ul>\n</li>\n<li><b>📄 收藏的帖子按钮（未来功能）：</b>\n<ul>\n<li>下载特定的收藏<i>帖子</i>（尤其是在它们是系列的一部分时，以类似漫画的顺序）是目前正在开发的功能。</li>\n<li>处理收藏帖子的最佳方式，特别是对于像漫画这样的顺序阅读，仍在探索中。</li>\n<li>如果您对如何下载和组织收藏帖子有具体的想法或用例（例如，从收藏中“漫画风格”），请考虑在项目的 GitHub 页面上提出问题或加入讨论。您的意见非常宝贵！</li>\n</ul>\n</li>\n<li><b>收藏下载范围（按钮）：</b>\n<ul>\n<li>此按钮（在“收藏的帖子”旁边）控制从所选收藏艺术家那里下载内容的位置：\n<ul>\n<li><b><i>范围：所选位置：</i></b>所有选定的艺术家都下载到您在界面中设置的主“下载位置”。筛选器全局应用于所有内容。</li>\n<li><b><i>范围：艺术家文件夹：</i></b>对于每个选定的艺术家，将在您的主“下载位置”内自动创建一个子文件夹（以艺术家命名）。该艺术家的内容将进入其特定的子文件夹。筛选器在每个艺术家的专用文件夹内应用。</li>\n</ul>\n</li>\n</ul>\n</li>\n<li><b>收藏模式下的筛选器：</b>\n<ul>\n<li>您在界面中设置的“🎯 按角色筛选”、“🚫 使用关键词跳过”和“筛选文件”选项仍将适用于从您选定的收藏艺术家那里下载的内容。</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step9_title":"⑨ 关键文件与导览",
"help_guide_step9_content":"<html><head/><body>\n<h3>应用程序使用的关键文件</h3>\n<ul>\n<li><b><code>Known.txt</code>：</b>\n<ul>\n<li>位于应用程序的目录中（<code>.exe</code> 或 <code>main.py</code> 所在的位置）。</li>\n<li>在启用“按名称/标题分文件夹”时，存储您已知的系列、角色或系列标题列表，用于自动文件夹组织。</li>\n<li><b>格式：</b>\n<ul>\n<li>每一行都是一个条目。</li>\n<li><b>简单名称：</b>例如，<code>我的精彩系列</code>。匹配此内容的内容将进入名为“我的精彩系列”的文件夹。</li>\n<li><b>分组别名：</b>例如，<code>(角色 A, 角色 A, 备用名 A)</code>。匹配“角色 A”、“角色 A”或“备用名 A”的内容将全部进入一个名为“角色 A 角色 A 备用名 A”的文件夹（清理后）。括号中的所有术语都成为该文件夹的别名。</li>\n</ul>\n</li>\n<li><b>用法：</b>如果帖子与您的活动“按角色筛选”输入不匹配，则用作文件夹命名的后备。您可以通过界面管理简单的条目，或直接编辑文件以获取复杂的别名。应用程序会在启动或下次使用时重新加载它。</li>\n</ul>\n</li>\n<li><b><code>cookies.txt</code>（可选）：</b>\n<ul>\n<li>如果您使用“使用 Cookie”功能并且不提供直接的 cookie 字符串或浏览到特定文件，应用程序将在其目录中查找名为 <code>cookies.txt</code> 的文件。</li>\n<li><b>格式：</b>必须是 Netscape cookie 文件格式。</li>\n<li><b>用法：</b>允许下载器使用您的浏览器的登录会话来访问可能需要在 Kemono/Coomer 上登录的内容。</li>\n</ul>\n</li>\n</ul>\n<h3>首次用户导览</h3>\n<ul>\n<li>在首次启动时（或如果重置），会出现一个欢迎导览对话框，引导您了解主要功能。您可以跳过它或选择“不再显示此导览”。</li>\n</ul>\n<p><em>许多界面元素还具有工具提示，当您将鼠标悬停在它们上面时会出现，提供快速提示。</em></p>\n</body></html>"
})

translations ["ru"]={}
translations ["ru"].update ({
"settings_dialog_title":"Настройки",
"language_label":"Язык:",
"lang_english":"Английский (English)",
"lang_japanese":"Японский (日本語)",
"theme_toggle_light":"Переключиться на светлый режим",
"theme_toggle_dark":"Переключиться на темный режим",
"theme_tooltip_light":"Изменить внешний вид приложения на светлый.",
"theme_tooltip_dark":"Изменить внешний вид приложения на темный.",
"ok_button":"ОК",
"appearance_group_title":"Внешний вид",
"language_group_title":"Языковые настройки",
"creator_post_url_label":"🔗 URL автора/поста Kemono:",
"download_location_label":"📁 Место для скачивания:",
"filter_by_character_label":"🎯 Фильтровать по персонажу(ам) (через запятую):",
"skip_with_words_label":"🚫 Пропускать со словами (через запятую):",
"remove_words_from_name_label":"✂️ Удалить слова из названия:",
"filter_all_radio":"Все",
"filter_images_radio":"Изображения/GIF",
"filter_videos_radio":"Видео",
"filter_archives_radio":"📦 Только архивы",
"filter_links_radio":"🔗 Только ссылки",
"filter_audio_radio":"🎧 Только аудио",
"favorite_mode_checkbox_label":"⭐ Режим избранного",
"browse_button_text":"Обзор...",
"char_filter_scope_files_text":"Фильтр: Файлы",
"char_filter_scope_files_tooltip":"Текущая область: Файлы\n\nФильтрует отдельные файлы по имени. Пост сохраняется, если совпадает хотя бы один файл.\nСкачиваются только совпадающие файлы из этого поста.\nПример: Фильтр 'Tifa'. Файл 'Tifa_artwork.jpg' совпадает и скачивается.\nИменование папок: Используется персонаж из совпадающего имени файла.\n\nНажмите для переключения на: Оба",
"char_filter_scope_title_text":"Фильтр: Заголовок",
"char_filter_scope_title_tooltip":"Текущая область: Заголовок\n\nФильтрует целые посты по их заголовку. Скачиваются все файлы из совпадающего поста.\nПример: Фильтр 'Aerith'. Пост с заголовком 'Сад Аэрис' совпадает; все его файлы скачиваются.\nИменование папок: Используется персонаж из совпадающего заголовка поста.\n\nНажмите для переключения на: Файлы",
"char_filter_scope_both_text":"Фильтр: Оба",
"char_filter_scope_both_tooltip":"Текущая область: Оба (сначала заголовок, затем файлы)\n\n1. Проверяет заголовок поста: Если совпадает, скачиваются все файлы из поста.\n2. Если заголовок не совпадает, проверяет имена файлов: Если совпадает какой-либо файл, скачивается только этот файл.\nПример: Фильтр 'Cloud'.\n - Пост 'Cloud Strife' (совпадение заголовка) -> скачиваются все файлы.\n - Пост 'Погоня на мотоцикле' с 'Cloud_fenrir.jpg' (совпадение файла) -> скачивается только 'Cloud_fenrir.jpg'.\nИменование папок: Приоритет отдается совпадению заголовка, затем совпадению файла.\n\nНажмите для переключения на: Комментарии",
"char_filter_scope_comments_text":"Фильтр: Комментарии (бета)",
"char_filter_scope_comments_tooltip":"Текущая область: Комментарии (бета - сначала файлы, затем комментарии в качестве запасного варианта)\n\n1. Проверяет имена файлов: Если какой-либо файл в посте совпадает с фильтром, скачивается весь пост. Комментарии НЕ проверяются на этот фильтрующий термин.\n2. Если файлы не совпадают, ТОГДА проверяет комментарии к посту: Если комментарий совпадает, скачивается весь пост.\nПример: Фильтр 'Barret'.\n - Пост А: Файлы 'Barret_gunarm.jpg', 'other.png'. Файл 'Barret_gunarm.jpg' совпадает. Все файлы из поста А скачиваются. Комментарии не проверяются на 'Barret'.\n - Пост Б: Файлы 'dyne.jpg', 'weapon.gif'. Комментарии: '...рисунок Баррета Уоллеса...'. Нет совпадений по файлам для 'Barret'. Комментарий совпадает. Все файлы из поста Б скачиваются.\nИменование папок: Приоритет отдается персонажу из совпадения файла, затем из совпадения комментария.\n\nНажмите для переключения на: Заголовок",
"char_filter_scope_unknown_text":"Фильтр: Неизвестно",
"char_filter_scope_unknown_tooltip":"Текущая область: Неизвестно\n\nОбласть фильтрации персонажей находится в неизвестном состоянии. Пожалуйста, переключите или сбросьте.\n\nНажмите для переключения на: Заголовок",
"skip_words_input_tooltip":"Введите слова через запятую, чтобы пропустить скачивание определенного контента (например, WIP, sketch, preview).\n\nКнопка 'Область: [Тип]' рядом с этим полем ввода циклически изменяет способ применения этого фильтра:\n- Область: Файлы: Пропускает отдельные файлы, если их имена содержат какие-либо из этих слов.\n- Область: Посты: Пропускает целые посты, если их заголовки содержат какие-либо из этих слов.\n- Область: Оба: Применяет оба (сначала заголовок поста, затем отдельные файлы, если заголовок поста подходит).",
"remove_words_input_tooltip":"Введите слова через запятую для удаления из имен скачиваемых файлов (без учета регистра).\nПолезно для очистки распространенных префиксов/суффиксов.\nПример: patreon, kemono, [HD], _final",
"skip_scope_files_text":"Область: Файлы",
"skip_scope_files_tooltip":"Текущая область пропуска: Файлы\n\nПропускает отдельные файлы, если их имена содержат какие-либо из 'Слов для пропуска'.\nПример: Слова для пропуска \"WIP, sketch\".\n- Файл \"art_WIP.jpg\" -> ПРОПУЩЕН.\n- Файл \"final_art.png\" -> СКАЧАН (если выполнены другие условия).\n\nПост по-прежнему обрабатывается на наличие других не пропущенных файлов.\nНажмите для переключения на: Оба",
"skip_scope_posts_text":"Область: Посты",
"skip_scope_posts_tooltip":"Текущая область пропуска: Посты\n\nПропускает целые посты, если их заголовки содержат какие-либо из 'Слов для пропуска'.\nВсе файлы из пропущенного поста игнорируются.\nПример: Слова для пропуска \"preview, announcement\".\n- Пост \"Захватывающее объявление!\" -> ПРОПУЩЕН.\n- Пост \"Готовое произведение искусства\" -> ОБРАБОТАН (если выполнены другие условия).\n\nНажмите для переключения на: Файлы",
"skip_scope_both_text":"Область: Оба",
"skip_scope_both_tooltip":"Текущая область пропуска: Оба (сначала посты, затем файлы)\n\n1. Проверяет заголовок поста: Если заголовок содержит слово для пропуска, весь пост ПРОПУСКАЕТСЯ.\n2. Если заголовок поста в порядке, проверяет имена отдельных файлов: Если имя файла содержит слово для пропуска, пропускается только этот файл.\nПример: Слова для пропуска \"WIP, sketch\".\n- Пост \"Эскизы и WIPs\" (совпадение заголовка) -> ВЕСЬ ПОСТ ПРОПУЩЕН.\n- Пост \"Обновление артов\" (заголовок в порядке) с файлами:\n  - \"character_WIP.jpg\" (совпадение файла) -> ПРОПУЩЕН.\n  - \"final_scene.png\" (файл в порядке) -> СКАЧАН.\n\nНажмите для переключения на: Посты",
"skip_scope_unknown_text":"Область: Неизвестно",
"skip_scope_unknown_tooltip":"Текущая область пропуска: Неизвестно\n\nОбласть слов для пропуска находится в неизвестном состоянии. Пожалуйста, переключите или сбросьте.\n\nНажмите для переключения на: Посты",
"language_change_title":"Язык изменен",
"language_change_message":"Язык был изменен. Для полного вступления изменений в силу требуется перезагрузка.",
"language_change_informative":"Хотите перезапустить приложение сейчас?",
"restart_now_button":"Перезапустить сейчас",
"skip_zip_checkbox_label":"Пропускать .zip",
"skip_rar_checkbox_label":"Пропускать .rar",
"download_thumbnails_checkbox_label":"Скачивать только миниатюры",
"scan_content_images_checkbox_label":"Сканировать контент на наличие изображений",
"compress_images_checkbox_label":"Сжимать в WebP",
"separate_folders_checkbox_label":"Раздельные папки по имени/заголовку",
"subfolder_per_post_checkbox_label":"Подпапка для каждого поста",
"use_cookie_checkbox_label":"Использовать cookie",
"use_multithreading_checkbox_base_label":"Использовать многопоточность",
"show_external_links_checkbox_label":"Показывать внешние ссылки в журнале",
"manga_comic_mode_checkbox_label":"Режим манги/комиксов",
"threads_label":"Потоки:",
"start_download_button_text":"⬇️ Начать скачивание",
"start_download_button_tooltip":"Нажмите, чтобы начать процесс скачивания или извлечения ссылок с текущими настройками.",
"extract_links_button_text":"🔗 Извлечь ссылки",
"pause_download_button_text":"⏸️ Приостановить скачивание",
"pause_download_button_tooltip":"Нажмите, чтобы приостановить текущий процесс скачивания.",
"resume_download_button_text":"▶️ Возобновить скачивание",
"resume_download_button_tooltip":"Нажмите, чтобы возобновить скачивание.",
"cancel_button_text":"❌ Отменить и сбросить интерфейс",
"cancel_button_tooltip":"Нажмите, чтобы отменить текущий процесс скачивания/извлечения и сбросить поля интерфейса (сохраняя URL и каталог).",
"error_button_text":"Ошибка",
"error_button_tooltip":"Просмотреть файлы, пропущенные из-за ошибок, и при необходимости повторить их скачивание.",
"cancel_retry_button_text":"❌ Отменить повтор",
"known_chars_label_text":"🎭 Известные шоу/персонажи (для названий папок):",
"open_known_txt_button_text":"Открыть Known.txt",
"known_chars_list_tooltip":"Этот список содержит имена, используемые для автоматического создания папок, когда включена опция 'Раздельные папки'\nи не указан или не совпадает с постом конкретный 'Фильтр по персонажу(ам)'.\nДобавьте названия сериалов, игр или персонажей, которые вы часто скачиваете.",
"open_known_txt_button_tooltip":"Открыть файл 'Known.txt' в вашем текстовом редакторе по умолчанию.\nФайл находится в каталоге приложения.",
"add_char_button_text":"➕ Добавить",
"add_char_button_tooltip":"Добавить имя из поля ввода в список 'Известные шоу/персонажи'.",
"add_to_filter_button_text":"⤵️ Добавить в фильтр",
"add_to_filter_button_tooltip":"Выберите имена из списка 'Известные шоу/персонажи', чтобы добавить их в поле 'Фильтровать по персонажу(ам)' выше.",
"delete_char_button_text":"🗑️ Удалить выбранные",
"delete_char_button_tooltip":"Удалить выбранные имена из списка 'Известные шоу/персонажи'.",
"progress_log_label_text":"� Журнал прогресса:",
"radio_all_tooltip":"Скачивать все типы файлов, найденные в постах.",
"radio_images_tooltip":"Скачивать только распространенные форматы изображений (JPG, PNG, GIF, WEBP и т. д.).",
"radio_videos_tooltip":"Скачивать только распространенные форматы видео (MP4, MKV, WEBM, MOV и т. д.).",
"radio_only_archives_tooltip":"Скачивать исключительно файлы .zip и .rar. Другие опции, специфичные для файлов, отключены.",
"radio_only_audio_tooltip":"Скачивать только распространенные аудиоформаты (MP3, WAV, FLAC и т. д.).",
"radio_only_links_tooltip":"Извлекать и отображать внешние ссылки из описаний постов вместо скачивания файлов.\nОпции, связанные со скачиванием, будут отключены.",
"favorite_mode_checkbox_tooltip":"Включить режим избранного для просмотра сохраненных художников/постов.\nЭто заменит поле ввода URL на кнопки выбора избранного.",
"skip_zip_checkbox_tooltip":"Если отмечено, архивные файлы .zip не будут скачиваться.\n(Отключено, если выбрано 'Только архивы').",
"skip_rar_checkbox_tooltip":"Если отмечено, архивные файлы .rar не будут скачиваться.\n(Отключено, если выбрано 'Только архивы').",
"download_thumbnails_checkbox_tooltip":"Скачивает небольшие изображения предварительного просмотра из API вместо полноразмерных файлов (если доступны).\nЕсли также отмечено 'Сканировать контент поста на наличие URL изображений', этот режим будет скачивать *только* изображения, найденные при сканировании контента (игнорируя миниатюры API).",
"scan_content_images_checkbox_tooltip":"Если отмечено, загрузчик будет сканировать HTML-содержимое постов на наличие URL-адресов изображений (из тегов <img> или прямых ссылок).\nЭто включает в себя преобразование относительных путей из тегов <img> в полные URL-адреса.\nОтносительные пути в тегах <img> (например, /data/image.jpg) будут преобразованы в полные URL-адреса.\nПолезно в случаях, когда изображения находятся в описании поста, но не в списке файлов/вложений API.",
"compress_images_checkbox_tooltip":"Сжимать изображения > 1,5 МБ в формат WebP (требуется Pillow).",
"use_subfolders_checkbox_tooltip":"Создавать подпапки на основе ввода 'Фильтровать по персонажу(ам)' или заголовков постов.\nИспользует список 'Известные шоу/персонажи' в качестве запасного варианта для названий папок, если конкретный фильтр не совпадает.\nВключает ввод 'Фильтровать по персонажу(ам)' и 'Пользовательское имя папки' для отдельных постов.",
"use_subfolder_per_post_checkbox_tooltip":"Создает подпапку для каждого поста. Если также включена опция 'Раздельные папки', она находится внутри папки персонажа/заголовка.",
"use_cookie_checkbox_tooltip":"Если отмечено, будет предпринята попытка использовать файлы cookie из 'cookies.txt' (формат Netscape)\nв каталоге приложения для запросов.\nПолезно для доступа к контенту, требующему входа в систему на Kemono/Coomer.",
"cookie_text_input_tooltip":"Введите вашу строку cookie напрямую.\nОна будет использована, если отмечено 'Использовать cookie' И 'cookies.txt' не найден или это поле не пустое.\nФормат зависит от того, как его будет разбирать бэкенд (например, 'name1=value1; name2=value2').",
"use_multithreading_checkbox_tooltip":"Включает параллельные операции. Подробности см. в поле 'Потоки'.",
"thread_count_input_tooltip":"Количество параллельных операций.\n- Один пост: параллельная загрузка файлов (рекомендуется 1-10).\n- URL ленты автора: количество постов для одновременной обработки (рекомендуется 1-200).\n  Файлы в каждом посте загружаются один за другим его рабочим потоком.\nЕсли 'Использовать многопоточность' не отмечено, используется 1 поток.",
"external_links_checkbox_tooltip":"Если отмечено, под основным журналом появится дополнительная панель журнала для отображения внешних ссылок, найденных в описаниях постов.\n(Отключено, если активен режим 'Только ссылки' или 'Только архивы').",
"manga_mode_checkbox_tooltip":"Скачивает посты от самых старых к самым новым и переименовывает файлы на основе заголовка поста (только для лент авторов).",
"multipart_on_button_text":"Многочаст.: ВКЛ",
"multipart_on_button_tooltip":"Многочастная загрузка: ВКЛ\n\nВключает одновременную загрузку больших файлов несколькими сегментами.\n- Может ускорить загрузку отдельных больших файлов (например, видео).\n- Может увеличить использование ЦП/сети.\n- Для лент с множеством мелких файлов это может не дать преимуществ в скорости и может сделать интерфейс/журнал перегруженным.\n- Если многочастная загрузка не удалась, она повторяется в однопоточном режиме.\n\nНажмите, чтобы ВЫКЛ.",
"multipart_off_button_text":"Многочаст.: ВЫКЛ",
"multipart_off_button_tooltip":"Многочастная загрузка: ВЫКЛ\n\nВсе файлы скачиваются одним потоком.\n- Стабильно и хорошо работает в большинстве случаев, особенно с множеством мелких файлов.\n- Большие файлы скачиваются последовательно.\n\nНажмите, чтобы ВКЛ (см. предупреждение).",
"reset_button_text":"🔄 Сброс",
"reset_button_tooltip":"Сбросить все вводы и журналы до состояния по умолчанию (только в режиме ожидания).",
"progress_idle_text":"Прогресс: Ожидание",
"missed_character_log_label_text":"🚫 Журнал пропущенных персонажей:",
"creator_popup_title":"Выбор автора",
"creator_popup_search_placeholder":"Искать по имени, сервису или вставить URL автора...",
"creator_popup_add_selected_button":"Добавить выбранные",
"creator_popup_scope_characters_button":"Область: Персонажи",
"creator_popup_scope_creators_button":"Область: Авторы",
"favorite_artists_button_text":"🖼️ Избранные художники",
"favorite_artists_button_tooltip":"Просматривайте и скачивайте работы ваших любимых художников на Kemono.su/Coomer.su.",
"favorite_posts_button_text":"📄 Избранные посты",
"favorite_posts_button_tooltip":"Просматривайте и скачивайте ваши любимые посты с Kemono.su/Coomer.su.",
"favorite_scope_selected_location_text":"Область: Выбранное место",
"favorite_scope_selected_location_tooltip":"Текущая область скачивания избранного: Выбранное место\n\nВсе выбранные избранные художники/посты будут скачаны в основное 'Место для скачивания', указанное в интерфейсе.\nФильтры (персонаж, слова для пропуска, тип файла) будут применяться глобально ко всему контенту.\n\nНажмите, чтобы изменить на: Папки художников",
"favorite_scope_artist_folders_text":"Область: Папки художников",
"favorite_scope_artist_folders_tooltip":"Текущая область скачивания избранного: Папки художников\n\nДля каждого выбранного избранного художника/поста будет создана новая подпапка (с именем художника) внутри основного 'Места для скачивания'.\nКонтент этого художника/поста будет скачан в их конкретную подпапку.\nФильтры (персонаж, слова для пропуска, тип файла) будут применяться *внутри* папки каждого художника.\n\nНажмите, чтобы изменить на: Выбранное место",
"favorite_scope_unknown_text":"Область: Неизвестно",
"favorite_scope_unknown_tooltip":"Область скачивания избранного неизвестна. Нажмите для переключения.",
"manga_style_post_title_text":"Название: Заголовок поста",
"manga_style_original_file_text":"Название: Исходный файл",
"manga_style_date_based_text":"Название: На основе даты",
"manga_style_title_global_num_text":"Название: Заголовок+Г.ном.",
"manga_style_unknown_text":"Название: Неизвестный стиль",
"fav_artists_dialog_title":"Избранные художники",
"fav_artists_loading_status":"Загрузка избранных художников...",
"fav_artists_search_placeholder":"Поиск художников...",
"fav_artists_select_all_button":"Выбрать все",
"fav_artists_deselect_all_button":"Снять выделение со всех",
"fav_artists_download_selected_button":"Скачать выбранные",
"fav_artists_cancel_button":"Отмена",
"fav_artists_loading_from_source_status":"⏳ Загрузка избранного из {source_name}...",
"fav_artists_found_status":"Найдено всего {count} избранных художников.",
"fav_artists_none_found_status":"На Kemono.su или Coomer.su не найдено избранных художников.",
"fav_artists_failed_status":"Не удалось загрузить избранное.",
"fav_artists_cookies_required_status":"Ошибка: Cookie включены, но не могут быть загружены ни для одного источника.",
"fav_artists_no_favorites_after_processing":"После обработки не найдено избранных художников.",
"fav_artists_no_selection_title":"Ничего не выбрано",
"fav_artists_no_selection_message":"Пожалуйста, выберите хотя бы одного художника для скачивания.",
"fav_posts_dialog_title":"Избранные посты",
"fav_posts_loading_status":"Загрузка избранных постов...",
"fav_posts_search_placeholder":"Поиск постов (заголовок, автор, ID, сервис)...",
"fav_posts_select_all_button":"Выбрать все",
"fav_posts_deselect_all_button":"Снять выделение со всех",
"fav_posts_download_selected_button":"Скачать выбранные",
"fav_posts_cancel_button":"Отмена",
"fav_posts_cookies_required_error":"Ошибка: для избранных постов требуются файлы cookie, но их не удалось загрузить.",
"fav_posts_auth_failed_title":"Ошибка авторизации (посты)",
"fav_posts_auth_failed_message":"Не удалось загрузить избранное{domain_specific_part} из-за ошибки авторизации:\n\n{error_message}\n\nЭто обычно означает, что ваши файлы cookie отсутствуют, недействительны или истек срок их действия для сайта. Пожалуйста, проверьте настройки cookie.",
"fav_posts_fetch_error_title":"Ошибка загрузки",
"fav_posts_fetch_error_message":"Ошибка загрузки избранного с {domain}{error_message_part}",
"fav_posts_no_posts_found_status":"Избранных постов не найдено.",
"fav_posts_found_status":"Найдено {count} избранных постов.",
"fav_posts_display_error_status":"Ошибка отображения постов: {error}",
"fav_posts_ui_error_title":"Ошибка интерфейса",
"fav_posts_ui_error_message":"Не удалось отобразить избранные посты: {error}",
"fav_posts_auth_failed_message_generic":"Не удалось загрузить избранное{domain_specific_part} из-за ошибки авторизации. Это обычно означает, что ваши файлы cookie отсутствуют, недействительны или истек срок их действия для сайта. Пожалуйста, проверьте настройки cookie.",
"key_fetching_fav_post_list_init":"Загрузка списка избранных постов...",
"key_fetching_from_source_kemono_su":"Загрузка избранного с Kemono.su...",
"key_fetching_from_source_coomer_su":"Загрузка избранного с Coomer.su...",
"fav_posts_fetch_cancelled_status":"Загрузка избранных постов отменена.",
"known_names_filter_dialog_title":"Добавить известные имена в фильтр",
"known_names_filter_search_placeholder":"Поиск имен...",
"known_names_filter_select_all_button":"Выбрать все",
"known_names_filter_deselect_all_button":"Снять выделение со всех",
"known_names_filter_add_selected_button":"Добавить выбранные",
"error_files_dialog_title":"Файлы, пропущенные из-за ошибок",
"error_files_no_errors_label":"Ни один файл не был записан как пропущенный из-за ошибок в последней сессии или после повторных попыток.",
"error_files_found_label":"Следующие {count} файлов были пропущены из-за ошибок скачивания:",
"error_files_select_all_button":"Выбрать все",
"error_files_retry_selected_button":"Повторить выбранные",
"error_files_export_urls_button":"Экспортировать URL в .txt",
"error_files_no_selection_retry_message":"Пожалуйста, выберите хотя бы один файл для повторной попытки.",
"error_files_no_errors_export_title":"Нет ошибок",
"error_files_no_errors_export_message":"Нет URL-адресов файлов с ошибками для экспорта.",
"error_files_no_urls_found_export_title":"URL не найдены",
"error_files_no_urls_found_export_message":"Не удалось извлечь URL-адреса из списка файлов с ошибками для экспорта.",
"error_files_save_dialog_title":"Сохранить URL-адреса файлов с ошибками",
"error_files_export_success_title":"Экспорт успешен",
"error_files_export_success_message":"Успешно экспортировано {count} записей в:\n{filepath}",
"error_files_export_error_title":"Ошибка экспорта",
"error_files_export_error_message":"Не удалось экспортировать ссылки на файлы: {error}",
"export_options_dialog_title":"Параметры экспорта",
"export_options_description_label":"Выберите формат для экспорта ссылок на файлы с ошибками:",
"export_options_radio_link_only":"Ссылка на строку (только URL)",
"export_options_radio_link_only_tooltip":"Экспортирует только прямую ссылку для скачивания каждого не удавшегося файла, по одной ссылке на строку.",
"export_options_radio_with_details":"Экспортировать с подробностями (URL [Пост, Информация о файле])",
"export_options_radio_with_details_tooltip":"Экспортирует URL, за которым следуют подробности, такие как заголовок поста, ID поста и исходное имя файла в скобках.",
"export_options_export_button":"Экспорт",
"no_errors_logged_title":"Ошибок не зарегистрировано",
"no_errors_logged_message":"Ни один файл не был записан как пропущенный из-за ошибок в последней сессии или после повторных попыток.",
"progress_initializing_text":"Прогресс: Инициализация...",
"progress_posts_text":"Прогресс: {processed_posts} / {total_posts} постов ({progress_percent:.1f}%)",
"progress_processing_post_text":"Прогресс: Обработка поста {processed_posts}...",
"progress_starting_text":"Прогресс: Запуск...",
"downloading_file_known_size_text":"Скачивание '{filename}' ({downloaded_mb:.1f}МБ / {total_mb:.1f}МБ)",
"downloading_file_unknown_size_text":"Скачивание '{filename}' ({downloaded_mb:.1f}МБ)",
"downloading_multipart_text":"Скач. '{filename}...': {downloaded_mb:.1f}/{total_mb:.1f} МБ ({parts} частей @ {speed:.2f} МБ/с)",
"downloading_multipart_initializing_text":"Файл: {filename} - Инициализация частей...",
"status_completed":"Завершено",
"status_cancelled_by_user":"Отменено пользователем",
"files_downloaded_label":"скачано",
"files_skipped_label":"пропущено",
"retry_finished_text":"Повторная попытка завершена",
"succeeded_text":"Успешно",
"failed_text":"Не удалось",
"ready_for_new_task_text":"Готов к новой задаче.",
"fav_mode_active_label_text":"⭐Выберите фильтры ниже, прежде чем выбрать понравившиеся.",
"export_links_button_text":"Экспортировать ссылки",
"download_extracted_links_button_text":"Скачать",
"download_selected_button_text":"Скачать выбранные",
"link_input_placeholder_text":"например, https://kemono.su/patreon/user/12345 или .../post/98765",
"link_input_tooltip_text":"Введите полный URL-адрес страницы автора Kemono/Coomer или конкретного поста.\nПример (Автор): https://kemono.su/patreon/user/12345\nПример (Пост): https://kemono.su/patreon/user/12345/post/98765",
"dir_input_placeholder_text":"Выберите папку, куда будут сохраняться скачанные файлы",
"dir_input_tooltip_text":"Введите или перейдите к основной папке, куда будет сохраняться весь скачанный контент.\nЭто поле является обязательным, если не выбран режим 'Только ссылки'.",
"character_input_placeholder_text":"например, Tifa, Aerith, (Cloud, Zack)",
"custom_folder_input_placeholder_text":"Необязательно: Сохранить этот пост в определенную папку",
"custom_folder_input_tooltip_text":"Если вы скачиваете URL-адрес одного поста И включена опция 'Раздельные папки по имени/заголовку',\nвы можете ввести здесь пользовательское имя для папки загрузки этого поста.\nПример: Моя любимая сцена",
"skip_words_input_placeholder_text":"например, WM, WIP, sketch, preview",
"remove_from_filename_input_placeholder_text":"например, patreon, HD",
"cookie_text_input_placeholder_no_file_selected_text":"Строка cookie (если не выбран cookies.txt)",
"cookie_text_input_placeholder_with_file_selected_text":"Использование выбранного файла cookie (см. Обзор...)",
"character_search_input_placeholder_text":"Поиск персонажей...",
"character_search_input_tooltip_text":"Введите здесь, чтобы отфильтровать список известных шоу/персонажей ниже.",
"new_char_input_placeholder_text":"Добавить новое название шоу/персонажа",
"new_char_input_tooltip_text":"Введите новое название шоу, игры или персонажа, чтобы добавить в список выше.",
"link_search_input_placeholder_text":"Поиск ссылок...",
"link_search_input_tooltip_text":"В режиме 'Только ссылки' введите здесь, чтобы отфильтровать отображаемые ссылки по тексту, URL или платформе.",
"manga_date_prefix_input_placeholder_text":"Префикс для имен файлов манги",
"manga_date_prefix_input_tooltip_text":"Необязательный префикс для имен файлов манги 'На основе даты' или 'Исходный файл' (например, 'Название серии').\nЕсли пусто, файлы будут названы в соответствии со стилем без префикса.",
"log_display_mode_links_view_text":"🔗 Просмотр ссылок",
"log_display_mode_progress_view_text":"⬇️ Просмотр прогресса",
"download_external_links_dialog_title":"Скачать выбранные внешние ссылки",
"select_all_button_text":"Выбрать все",
"deselect_all_button_text":"Снять выделение со всех",
"cookie_browse_button_tooltip":"Обзор файла cookie (формат Netscape, обычно cookies.txt).\nОн будет использован, если отмечено 'Использовать cookie' и текстовое поле выше пустое.",
"page_range_label_text":"Диапазон страниц:",
"start_page_input_placeholder":"Начало",
"start_page_input_tooltip":"Для URL авторов: Укажите начальный номер страницы для скачивания (например, 1, 2, 3).\nОставьте пустым или установите 1, чтобы начать с первой страницы.\nОтключено для URL отдельных постов или в режиме манги/комиксов.",
"page_range_to_label_text":"до",
"end_page_input_placeholder":"Конец",
"end_page_input_tooltip":"Для URL авторов: Укажите конечный номер страницы для скачивания (например, 5, 10).\nОставьте пустым, чтобы скачать все страницы с начальной страницы.\nОтключено для URL отдельных постов или в режиме манги/комиксов.",
"known_names_help_button_tooltip_text":"Открыть руководство по функциям приложения.",
"future_settings_button_tooltip_text":"Открыть настройки приложения (тема, язык и т. д.).",
"link_search_button_tooltip_text":"Фильтровать отображаемые ссылки",
"confirm_add_all_dialog_title":"Подтвердить добавление новых имен",
"confirm_add_all_info_label":"Следующие новые имена/группы из вашего ввода 'Фильтровать по персонажу(ам)' отсутствуют в 'Known.txt'.\nИх добавление может улучшить организацию папок для будущих загрузок.\n\nПросмотрите список и выберите действие:",
"confirm_add_all_select_all_button":"Выбрать все",
"confirm_add_all_deselect_all_button":"Снять выделение со всех",
"confirm_add_all_add_selected_button":"Добавить выбранные в Known.txt",
"confirm_add_all_skip_adding_button":"Пропустить добавление этих",
"confirm_add_all_cancel_download_button":"Отменить скачивание",
"cookie_help_dialog_title":"Инструкции по файлу cookie",
"cookie_help_instruction_intro":"<p>Для использования файлов cookie обычно требуется файл <b>cookies.txt</b> из вашего браузера.</p>",
"cookie_help_how_to_get_title":"<p><b>Как получить cookies.txt:</b></p>",
"cookie_help_step1_extension_intro":"<li>Установите расширение 'Get cookies.txt LOCALLY' для вашего браузера на основе Chrome:<br><a href=\"https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc\" style=\"color: #87CEEB;\">Получить cookies.txt LOCALLY в Chrome Web Store</a></li>",
"cookie_help_step2_login":"<li>Перейдите на веб-сайт (например, kemono.su или coomer.su) и при необходимости войдите в систему.</li>",
"cookie_help_step3_click_icon":"<li>Нажмите на значок расширения на панели инструментов вашего браузера.</li>",
"cookie_help_step4_export":"<li>Нажмите кнопку 'Экспорт' (например, 'Экспортировать как', 'Экспортировать cookies.txt' - точная формулировка может отличаться в зависимости от версии расширения).</li>",
"cookie_help_step5_save_file":"<li>Сохраните загруженный файл <code>cookies.txt</code> на свой компьютер.</li>",
"cookie_help_step6_app_intro":"<li>В этом приложении:<ul>",
"cookie_help_step6a_checkbox":"<li>Убедитесь, что установлен флажок 'Использовать cookie'.</li>",
"cookie_help_step6b_browse":"<li>Нажмите кнопку 'Обзор...' рядом с текстовым полем cookie.</li>",
"cookie_help_step6c_select":"<li>Выберите только что сохраненный файл <code>cookies.txt</code>.</li></ul></li>",
"cookie_help_alternative_paste":"<p>Кроме того, некоторые расширения могут позволить вам скопировать строку cookie напрямую. В этом случае вы можете вставить ее в текстовое поле вместо просмотра файла.</p>",
"cookie_help_proceed_without_button":"Скачать без файлов cookie",
"empty_popup_button_tooltip_text": "Открыть выбор автора (Обзор creators.json)",
"cookie_help_cancel_download_button":"Отменить скачивание",
"character_input_tooltip":"Введите имена персонажей (через запятую). Поддерживает расширенную группировку и влияет на именование папок, если включена опция 'Раздельные папки'.\n\nПримеры:\n- Nami → Совпадает с 'Nami', создает папку 'Nami'.\n- (Ulti, Vivi) → Совпадает с любым из них, папка 'Ulti Vivi', добавляет оба в Known.txt отдельно.\n- (Boa, Hancock)~ → Совпадает с любым из них, папка 'Boa Hancock', добавляет как одну группу в Known.txt.\n\nИмена рассматриваются как псевдонимы для сопоставления.\n\nРежимы фильтра (кнопка переключает):\n- Файлы: Фильтрует по имени файла.\n- Заголовок: Фильтрует по заголовку поста.\n- Оба: Сначала заголовок, затем имя файла.\n- Комментарии (бета): Сначала имя файла, затем комментарии к посту.",
"tour_dialog_title":"Добро пожаловать в Kemono Downloader!",
"tour_dialog_never_show_checkbox":"Больше не показывать это руководство",
"tour_dialog_skip_button":"Пропустить руководство",
"tour_dialog_back_button":"Назад",
"tour_dialog_next_button":"Далее",
"tour_dialog_finish_button":"Готово",
"tour_dialog_step1_title":"👋 Добро пожаловать!",
"tour_dialog_step1_content":"Здравствуйте! Этот краткий обзор проведет вас по основным функциям Kemono Downloader, включая последние обновления, такие как улучшенная фильтрация, улучшения режима манги и управление файлами cookie.\n<ul>\n<li>Моя цель - помочь вам легко скачивать контент с <b>Kemono</b> и <b>Coomer</b>.</li><br>\n<li><b>🎨 Кнопка выбора автора:</b> Рядом с полем ввода URL нажмите на значок палитры, чтобы открыть диалоговое окно. Просмотрите и выберите авторов из вашего файла <code>creators.json</code>, чтобы быстро добавить их имена в поле ввода URL.</li><br>\n<li><b>Важный совет: Приложение '(Не отвечает)'?</b><br>\nПосле нажатия 'Начать скачивание', особенно для больших лент авторов или с большим количеством потоков, приложение может временно отображаться как '(Не отвечает)'. Ваша операционная система (Windows, macOS, Linux) может даже предложить вам 'Завершить процесс' или 'Принудительно завершить'.<br>\n<b>Пожалуйста, будьте терпеливы!</b> Приложение часто все еще усердно работает в фоновом режиме. Прежде чем принудительно закрывать, попробуйте проверить выбранное 'Место для скачивания' в вашем файловом менеджере. Если вы видите, что создаются новые папки или появляются файлы, это означает, что скачивание идет правильно. Дайте ему немного времени, чтобы снова стать отзывчивым.</li><br>\n<li>Используйте кнопки <b>Далее</b> и <b>Назад</b> для навигации.</li><br>\n<li>Многие опции имеют всплывающие подсказки, если вы наведете на них курсор, для получения дополнительной информации.</li><br>\n<li>Нажмите <b>Пропустить руководство</b>, чтобы закрыть это руководство в любое время.</li><br>\n<li>Установите флажок <b>'Больше не показывать это руководство'</b>, если вы не хотите видеть его при будущих запусках.</li>\n</ul>",
"tour_dialog_step2_title":"① Начало работы",
"tour_dialog_step2_content":"Давайте начнем с основ скачивания:\n<ul>\n<li><b>🔗 URL автора/поста Kemono:</b><br>\nВставьте полный веб-адрес (URL) страницы автора (например, <i>https://kemono.su/patreon/user/12345</i>)\nили конкретного поста (например, <i>.../post/98765</i>).<br>\nили автора Coomer (например, <i>https://coomer.su/onlyfans/user/artistname</i>)</li><br>\n<li><b>📁 Место для скачивания:</b><br>\nНажмите 'Обзор...', чтобы выбрать папку на вашем компьютере, куда будут сохраняться все скачанные файлы.\nЭто поле является обязательным, если вы не используете режим 'Только ссылки'.</li><br>\n<li><b>📄 Диапазон страниц (только URL автора):</b><br>\nЕсли вы скачиваете со страницы автора, вы можете указать диапазон страниц для загрузки (например, страницы со 2 по 5).\nОставьте пустым для всех страниц. Эта опция отключена для URL отдельных постов или когда активен <b>Режим манги/комиксов</b>.</li>\n</ul>",
"tour_dialog_step3_title":"② Фильтрация загрузок",
"tour_dialog_step3_content":"Уточните, что вы скачиваете, с помощью этих фильтров (большинство из них отключены в режимах 'Только ссылки' или 'Только архивы'):\n<ul>\n<li><b>🎯 Фильтровать по персонажу(ам):</b><br>\nВведите имена персонажей через запятую (например, <i>Tifa, Aerith</i>). Сгруппируйте псевдонимы для общего имени папки: <i>(псевдоним1, псевдоним2, псевдоним3)</i> становится папкой 'псевдоним1 псевдоним2 псевдоним3' (после очистки). Все имена в группе используются как псевдонимы для сопоставления.<br>\nКнопка <b>'Фильтр: [Тип]'</b> (рядом с этим полем ввода) циклически изменяет способ применения этого фильтра:\n<ul><li><i>Фильтр: Файлы:</i> Проверяет имена отдельных файлов. Пост сохраняется, если совпадает хотя бы один файл; скачиваются только совпадающие файлы. Именование папок использует персонажа из совпадающего имени файла (если включена опция 'Раздельные папки').</li><br>\n<li><i>Фильтр: Заголовок:</i> Проверяет заголовки постов. Скачиваются все файлы из совпадающего поста. Именование папок использует персонажа из совпадающего заголовка поста.</li>\n<li><b>⤵️ Кнопка 'Добавить в фильтр' (Известные имена):</b> Рядом с кнопкой 'Добавить' для известных имен (см. Шаг 5), это открывает всплывающее окно. Выберите имена из вашего списка <code>Known.txt</code> с помощью флажков (с панелью поиска), чтобы быстро добавить их в поле 'Фильтровать по персонажу(ам)'. Сгруппированные имена, такие как <code>(Boa, Hancock)</code> из Known.txt, будут добавлены в фильтр как <code>(Boa, Hancock)~</code>.</li><br>\n<li><i>Фильтр: Оба:</i> Сначала проверяет заголовок поста. Если он совпадает, скачиваются все файлы. Если нет, то проверяет имена файлов, и скачиваются только совпадающие файлы. Именование папок отдает приоритет совпадению заголовка, затем совпадению файла.</li><br>\n<li><i>Фильтр: Комментарии (бета):</i> Сначала проверяет имена файлов. Если файл совпадает, скачиваются все файлы из поста. Если совпадения по файлам нет, то проверяет комментарии к посту. Если комментарий совпадает, скачиваются все файлы. (Использует больше запросов к API). Именование папок отдает приоритет совпадению файла, затем совпадению комментария.</li></ul>\nЭтот фильтр также влияет на именование папок, если включена опция 'Раздельные папки по имени/заголовку'.</li><br>\n<li><b>🚫 Пропускать со словами:</b><br>\nВведите слова через запятую (например, <i>WIP, sketch, preview</i>).\nКнопка <b>'Область: [Тип]'</b> (рядом с этим полем ввода) циклически изменяет способ применения этого фильтра:\n<ul><li><i>Область: Файлы:</i> Пропускает файлы, если их имена содержат какие-либо из этих слов.</li><br>\n<li><i>Область: Посты:</i> Пропускает целые посты, если их заголовки содержат какие-либо из этих слов.</li><br>\n<li><i>Область: Оба:</i> Применяет пропуск как по названию файла, так и по заголовку поста (сначала пост, затем файлы).</li></ul></li><br>\n<li><b>Фильтровать файлы (Радиокнопки):</b> Выберите, что скачивать:\n<ul>\n<li><i>Все:</i> Скачивает все найденные типы файлов.</li><br>\n<li><i>Изображения/GIF:</i> Только распространенные форматы изображений и GIF.</li><br>\n<li><i>Видео:</i> Только распространенные форматы видео.</li><br>\n<li><b><i>📦 Только архивы:</i></b> Скачивает исключительно файлы <b>.zip</b> и <b>.rar</b>. При выборе этой опции флажки 'Пропускать .zip' и 'Пропускать .rar' автоматически отключаются и снимаются. 'Показывать внешние ссылки' также отключается.</li><br>\n<li><i>🎧 Только аудио:</i> Только распространенные аудиоформаты (MP3, WAV, FLAC и т. д.).</li><br>\n<li><i>🔗 Только ссылки:</i> Извлекает и отображает внешние ссылки из описаний постов вместо скачивания файлов. Опции, связанные со скачиванием, и 'Показывать внешние ссылки' отключаются.</li>\n</ul></li>\n</ul>",
"tour_dialog_step4_title":"③ Режим избранного (альтернативная загрузка)",
"tour_dialog_step4_content":"Приложение предлагает 'Режим избранного' для скачивания контента от художников, которых вы добавили в избранное на Kemono.su.\n<ul>\n<li><b>⭐ Флажок 'Режим избранного':</b><br>\nРасположен рядом с радиокнопкой '🔗 Только ссылки'. Установите этот флажок, чтобы активировать режим избранного.</li><br>\n<li><b>Что происходит в режиме избранного:</b>\n<ul><li>Область ввода '🔗 URL автора/поста Kemono' заменяется сообщением о том, что режим избранного активен.</li><br>\n<li>Стандартные кнопки 'Начать скачивание', 'Пауза', 'Отмена' заменяются кнопками '🖼️ Избранные художники' и '📄 Избранные посты' (Примечание: 'Избранные посты' планируется в будущем).</li><br>\n<li>Опция '🍪 Использовать cookie' автоматически включается и блокируется, так как для загрузки избранного требуются файлы cookie.</li></ul></li><br>\n<li><b>🖼️ Кнопка 'Избранные художники':</b><br>\nНажмите эту кнопку, чтобы открыть диалоговое окно со списком ваших избранных художников с Kemono.su. Вы можете выбрать одного или нескольких художников для скачивания.</li><br>\n<li><b>Область скачивания избранного (Кнопка):</b><br>\nЭта кнопка (рядом с 'Избранными постами') управляет тем, куда скачивается выбранное избранное:\n<ul><li><i>Область: Выбранное место:</i> Все выбранные художники скачиваются в основное 'Место для скачивания', которое вы установили. Фильтры применяются глобально.</li><br>\n<li><i>Область: Папки художников:</i> В вашем основном 'Месте для скачивания' для каждого выбранного художника создается подпапка (с именем художника). Контент этого художника попадает в его конкретную папку. Фильтры применяются внутри папки каждого художника.</li></ul></li><br>\n<li><b>Фильтры в режиме избранного:</b><br>\nОпции 'Фильтровать по персонажу(ам)', 'Пропускать со словами' и 'Фильтровать файлы' по-прежнему применяются к контенту, скачиваемому от ваших избранных художников.</li>\n</ul>",
"tour_dialog_step5_title":"④ Тонкая настройка загрузок",
"tour_dialog_step5_content":"Дополнительные опции для настройки ваших загрузок:\n<ul>\n<li><b>Пропускать .zip / Пропускать .rar:</b> Установите эти флажки, чтобы избежать скачивания этих типов архивных файлов.\n<i>(Примечание: Они отключены и игнорируются, если выбран режим фильтра '📦 Только архивы').</i></li><br>\n<li><b>✂️ Удалить слова из названия:</b><br>\nВведите слова через запятую (например, <i>patreon, [HD]</i>) для удаления из имен скачиваемых файлов (без учета регистра).</li><br>\n<li><b>Скачивать только миниатюры:</b> Скачивает небольшие изображения предварительного просмотра вместо полноразмерных файлов (если доступны).</li><br>\n<li><b>Сжимать большие изображения:</b> Если установлена библиотека 'Pillow', изображения размером более 1,5 МБ будут преобразованы в формат WebP, если версия WebP значительно меньше.</li><br>\n<li><b>🗄️ Пользовательское имя папки (только для одного поста):</b><br>\nЕсли вы скачиваете URL-адрес одного конкретного поста И включена опция 'Раздельные папки по имени/заголовку',\nвы можете ввести здесь пользовательское имя для папки загрузки этого поста.</li><br>\n<li><b>🍪 Использовать cookie:</b> Установите этот флажок для использования файлов cookie для запросов. Вы можете либо:\n<ul><li>Ввести строку cookie непосредственно в текстовое поле (например, <i>name1=value1; name2=value2</i>).</li><br>\n<li>Нажать 'Обзор...', чтобы выбрать файл <i>cookies.txt</i> (формат Netscape). Путь появится в текстовом поле.</li></ul>\nЭто полезно для доступа к контенту, требующему входа в систему. Текстовое поле имеет приоритет, если оно заполнено.\nЕсли флажок 'Использовать cookie' установлен, но и текстовое поле, и просматриваемый файл пусты, он попытается загрузить 'cookies.txt' из каталога приложения.</li>\n</ul>",
"tour_dialog_step6_title":"⑤ Организация и производительность",
"tour_dialog_step6_content":"Организуйте свои загрузки и управляйте производительностью:\n<ul>\n<li><b>⚙️ Раздельные папки по имени/заголовку:</b> Создает подпапки на основе ввода 'Фильтровать по персонажу(ам)' или заголовков постов (может использовать список <b>Known.txt</b> в качестве запасного варианта для названий папок).</li><br>\n<li><b>Подпапка для каждого поста:</b> Если опция 'Раздельные папки' включена, это создает дополнительную подпапку для <i>каждого отдельного поста</i> внутри основной папки персонажа/заголовка.</li><br>\n<li><b>🚀 Использовать многопоточность (Потоки):</b> Включает более быстрые операции. Число в поле 'Потоки' означает:\n<ul><li>Для <b>Лент авторов:</b> Количество постов для одновременной обработки. Файлы в каждом посте скачиваются последовательно его рабочим потоком (если не включено именование манги 'На основе даты', что принудительно использует 1 рабочий поток для поста).</li><br>\n<li>Для <b>URL отдельных постов:</b> Количество файлов для одновременной загрузки из этого одного поста.</li></ul>\nЕсли флажок не установлен, используется 1 поток. Высокое количество потоков (например, >40) может показать предупреждение.</li><br>\n<li><b>Переключатель многочастной загрузки (верхний правый угол области журнала):</b><br>\nКнопка <b>'Многочаст.: [ВКЛ/ВЫКЛ]'</b> позволяет включать/отключать многосегментную загрузку для отдельных больших файлов.\n<ul><li><b>ВКЛ:</b> Может ускорить загрузку больших файлов (например, видео), но может увеличить 'дерганье' интерфейса или спам в журнале при большом количестве мелких файлов. При включении появляется предупреждение. Если многочастная загрузка не удалась, она повторяется в однопоточном режиме.</li><br>\n<li><b>ВЫКЛ (по умолчанию):</b> Файлы скачиваются одним потоком.</li></ul>\nЭта опция отключена, если активен режим 'Только ссылки' или 'Только архивы'.</li><br>\n<li><b>📖 Режим манги/комиксов (только URL автора):</b> Специально для последовательного контента.\n<ul>\n<li>Скачивает посты от <b>самых старых к самым новым</b>.</li><br>\n<li>Поле 'Диапазон страниц' отключено, так как скачиваются все посты.</li><br>\n<li>Кнопка <b>переключения стиля имени файла</b> (например, 'Название: Заголовок поста') появляется в верхнем правом углу области журнала, когда этот режим активен для ленты автора. Нажмите ее, чтобы переключаться между стилями именования:\n<ul>\n<li><b><i>Название: Заголовок поста (по умолчанию):</i></b> Первый файл в посте называется по очищенному заголовку поста (например, 'Моя глава 1.jpg'). Последующие файлы в *том же посте* попытаются сохранить свои исходные имена файлов (например, 'page_02.png', 'bonus_art.jpg'). Если в посте только один файл, он называется по заголовку поста. Это обычно рекомендуется для большинства манг/комиксов.</li><br>\n<li><b><i>Название: Исходный файл:</i></b> Все файлы пытаются сохранить свои исходные имена файлов. Необязательный префикс (например, 'МояСерия_') можно ввести в поле ввода, которое появляется рядом с кнопкой стиля. Пример: 'МояСерия_ИсходныйФайл.jpg'.</li><br>\n<li><b><i>Название: Заголовок+Г.ном. (Заголовок поста + Глобальная нумерация):</i></b> Все файлы во всех постах текущей сессии скачивания именуются последовательно с использованием очищенного заголовка поста в качестве префикса, за которым следует глобальный счетчик. Например: Пост 'Глава 1' (2 файла) -> 'Глава 1_001.jpg', 'Глава 1_002.png'. Следующий пост 'Глава 2' (1 файл) продолжит нумерацию -> 'Глава 2_003.jpg'. Многопоточность для обработки постов автоматически отключается для этого стиля, чтобы обеспечить правильную глобальную нумерацию.</li><br>\n<li><b><i>Название: На основе даты:</i></b> Файлы именуются последовательно (001.ext, 002.ext, ...) на основе порядка публикации постов. Необязательный префикс (например, 'МояСерия_') можно ввести в поле ввода, которое появляется рядом с кнопкой стиля. Пример: 'МояСерия_001.jpg'. Многопоточность для обработки постов автоматически отключается для этого стиля.</li>\n</ul>\n</li><br>\n<li>Для достижения наилучших результатов со стилями 'Название: Заголовок поста', 'Название: Заголовок+Г.ном.' или 'Название: На основе даты' используйте поле 'Фильтровать по персонажу(ам)' с названием манги/серии для организации папок.</li>\n</ul></li><br>\n<li><b>🎭 Known.txt для умной организации папок:</b><br>\n<code>Known.txt</code> (в каталоге приложения) позволяет точно контролировать автоматическую организацию папок, когда включена опция 'Раздельные папки по имени/заголовку'.\n<ul>\n<li><b>Как это работает:</b> Каждая строка в <code>Known.txt</code> является записью.\n<ul><li>Простая строка, такая как <code>Моя потрясающая серия</code>, означает, что контент, соответствующий этому, попадет в папку с названием 'Моя потрясающая серия'.</li><br>\n<li>Сгруппированная строка, такая как <code>(Персонаж А, Перс А, Альтернативное имя А)</code>, означает, что контент, соответствующий 'Персонаж А', 'Перс А' ИЛИ 'Альтернативное имя А', попадет в ОДНУ папку с названием 'Персонаж А Перс А Альтернативное имя А' (после очистки). Все термины в скобках становятся псевдонимами для этой папки.</li></ul></li>\n<li><b>Интеллектуальный запасной вариант:</b> Когда опция 'Раздельные папки по имени/заголовку' активна, и если пост не соответствует какому-либо конкретному вводу 'Фильтровать по персонажу(ам)', загрузчик обращается к <code>Known.txt</code>, чтобы найти соответствующее основное имя для создания папки.</li><br>\n<li><b>Удобное управление:</b> Добавляйте простые (не сгруппированные) имена через список в интерфейсе ниже. Для расширенного редактирования (например, создания/изменения сгруппированных псевдонимов) нажмите <b>'Открыть Known.txt'</b>, чтобы отредактировать файл в вашем текстовом редакторе. Приложение перезагружает его при следующем использовании или запуске.</li>\n</ul>\n</li>\n</ul>",
"tour_dialog_step7_title":"⑥ Распространенные ошибки и устранение неполадок",
"tour_dialog_step7_content":"Иногда при загрузке могут возникать проблемы. Вот несколько распространенных:\n<ul>\n<li><b>Подсказка для ввода персонажа:</b><br>\nВведите имена персонажей через запятую (например, <i>Tifa, Aerith</i>).<br>\nСгруппируйте псевдонимы для общего имени папки: <i>(псевдоним1, псевдоним2, псевдоним3)</i> становится папкой 'псевдоним1 псевдоним2 псевдоним3'.<br>\nВсе имена в группе используются как псевдонимы для сопоставления контента.<br><br>\nКнопка 'Фильтр: [Тип]' рядом с этим полем ввода циклически изменяет способ применения этого фильтра:<br>\n- Фильтр: Файлы: Проверяет имена отдельных файлов. Скачиваются только совпадающие файлы.<br>\n- Фильтр: Заголовок: Проверяет заголовки постов. Скачиваются все файлы из совпадающего поста.<br>\n- Фильтр: Оба: Сначала проверяет заголовок поста. Если совпадения нет, то проверяет имена файлов.<br>\n- Фильтр: Комментарии (бета): Сначала проверяет имена файлов. Если совпадения нет, то проверяет комментарии к посту.<br><br>\nЭтот фильтр также влияет на именование папок, если включена опция 'Раздельные папки по имени/заголовку'.</li><br>\n<li><b>502 Bad Gateway / 503 Service Unavailable / 504 Gateway Timeout:</b><br>\nЭто обычно указывает на временные проблемы на стороне сервера с Kemono/Coomer. Сайт может быть перегружен, находиться на обслуживании или испытывать проблемы.<br>\n<b>Решение:</b> Подождите некоторое время (например, от 30 минут до нескольких часов) и попробуйте снова позже. Проверьте сайт непосредственно в вашем браузере.</li><br>\n<li><b>Потеряно соединение / Соединение отклонено / Тайм-аут (во время загрузки файла):</b><br>\nЭто может произойти из-за вашего интернет-соединения, нестабильности сервера или если сервер разрывает соединение для большого файла.<br>\n<b>Решение:</b> Проверьте ваше интернет-соединение. Попробуйте уменьшить количество 'Потоков', если оно велико. Приложение может предложить повторить некоторые неудачные файлы в конце сеанса.</li><br>\n<li><b>Ошибка IncompleteRead:</b><br>\nСервер отправил меньше данных, чем ожидалось. Часто это временный сбой сети или проблема с сервером.<br>\n<b>Решение:</b> Приложение часто помечает эти файлы для повторной попытки в конце сеанса загрузки.</li><br>\n<li><b>403 Forbidden / 401 Unauthorized (реже для общедоступных постов):</b><br>\nУ вас может не быть разрешения на доступ к контенту. Для некоторого платного или частного контента может помочь использование опции 'Использовать cookie' с действительными файлами cookie из вашей сессии браузера. Убедитесь, что ваши файлы cookie свежие.</li><br>\n<li><b>404 Not Found:</b><br>\nURL поста или файла неверен, или контент был удален с сайта. Дважды проверьте URL.</li><br>\n<li><b>'Постов не найдено' / 'Целевой пост не найден':</b><br>\nУбедитесь, что URL правильный и автор/пост существует. Если вы используете диапазоны страниц, убедитесь, что они действительны для автора. Для очень новых постов может быть небольшая задержка, прежде чем они появятся в API.</li><br>\n<li><b>Общая медлительность / Приложение '(Не отвечает)':</b><br>\nКак упоминалось в Шаге 1, если приложение кажется зависшим после запуска, особенно с большими лентами авторов или большим количеством потоков, пожалуйста, дайте ему время. Вероятно, оно обрабатывает данные в фоновом режиме. Уменьшение количества потоков иногда может улучшить отзывчивость, если это происходит часто.</li>\n</ul>",
"tour_dialog_step8_title":"⑦ Журнал и финальные элементы управления",
"tour_dialog_step8_content":"Мониторинг и элементы управления:\n<ul>\n<li><b>📜 Журнал прогресса / Журнал извлеченных ссылок:</b> Показывает подробные сообщения о загрузке. Если активен режим '🔗 Только ссылки', эта область отображает извлеченные ссылки.</li><br>\n<li><b>Показывать внешние ссылки в журнале:</b> Если отмечено, под основным журналом появится дополнительная панель журнала для отображения любых внешних ссылок, найденных в описаниях постов. <i>(Эта опция отключена, если активен режим '🔗 Только ссылки' или '📦 Только архивы').</i></li><br>\n<li><b>Переключатель вида журнала (Кнопка 👁️ / 🙈):</b><br>\nЭта кнопка (в верхнем правом углу области журнала) переключает вид основного журнала:\n<ul><li><b>👁️ Журнал прогресса (по умолчанию):</b> Показывает всю активность загрузки, ошибки и сводки.</li><br>\n<li><b>🙈 Журнал пропущенных персонажей:</b> Отображает список ключевых терминов из заголовков постов, которые были пропущены из-за ваших настроек 'Фильтровать по персонажу(ам)'. Полезно для выявления контента, который вы можете непреднамеренно пропускать.</li></ul></li><br>\n<li><b>🔄 Сброс:</b> Очищает все поля ввода, журналы и сбрасывает временные настройки до их значений по умолчанию. Может использоваться только тогда, когда загрузка не активна.</li><br>\n<li><b>⬇️ Начать скачивание / 🔗 Извлечь ссылки / ⏸️ Пауза / ❌ Отмена:</b> Эти кнопки управляют процессом. 'Отменить и сбросить интерфейс' останавливает текущую операцию и выполняет мягкий сброс интерфейса, сохраняя ваши вводы URL и каталога. 'Пауза/Возобновить' позволяет временно останавливать и продолжать.</li><br>\n<li>Если некоторые файлы завершаются сбоем с устранимыми ошибками (например, 'IncompleteRead'), вам может быть предложено повторить их в конце сеанса.</li>\n</ul>\n<br>Вы готовы! Нажмите <b>'Готово'</b>, чтобы закрыть руководство и начать использовать загрузчик.",
"help_guide_dialog_title":"Kemono Downloader - Руководство по функциям",
"help_guide_github_tooltip":"Посетить страницу проекта на GitHub (открывается в браузере)",
"help_guide_instagram_tooltip":"Посетить нашу страницу в Instagram (открывается в браузере)",
"help_guide_discord_tooltip":"Посетить наше сообщество в Discord (открывается в браузере)",
"help_guide_step1_title":"① Введение и основные поля ввода",
"help_guide_step1_content":"<html><head/><body>\n<p>Это руководство представляет обзор функций, полей и кнопок Kemono Downloader.</p>\n<h3>Основная область ввода (вверху слева)</h3>\n<ul>\n<li><b>🔗 URL автора/поста Kemono:</b>\n<ul>\n<li>Введите полный веб-адрес страницы автора (например, <i>https://kemono.su/patreon/user/12345</i>) или конкретного поста (например, <i>.../post/98765</i>).</li>\n<li>Поддерживает URL-адреса Kemono (kemono.su, kemono.party) и Coomer (coomer.su, coomer.party).</li>\n</ul>\n</li>\n<li><b>Диапазон страниц (от и до):</b>\n<ul>\n<li>Для URL-адресов авторов: укажите диапазон страниц для загрузки (например, со 2 по 5 страницу). Оставьте пустым для всех страниц.</li>\n<li>Отключено для URL-адресов отдельных постов или когда активен <b>Режим манги/комиксов</b>.</li>\n</ul>\n</li>\n<li><b>📁 Место для скачивания:</b>\n<ul>\n<li>Нажмите <b>'Обзор...'</b>, чтобы выбрать основную папку на вашем компьютере, куда будут сохраняться все скачанные файлы.</li>\n<li>Это поле обязательно, если вы не используете режим <b>'🔗 Только ссылки'</b>.</li>\n</ul>\n</li>\n<li><b>🎨 Кнопка выбора автора (рядом с полем ввода URL):</b>\n<ul>\n<li>Нажмите на значок палитры (🎨), чтобы открыть диалоговое окно 'Выбор автора'.</li>\n<li>Это диалоговое окно загружает авторов из вашего файла <code>creators.json</code> (который должен находиться в каталоге приложения).</li>\n<li><b>Внутри диалогового окна:</b>\n<ul>\n<li><b>Панель поиска:</b> Введите текст для фильтрации списка авторов по имени или сервису.</li>\n<li><b>Список авторов:</b> Отображает авторов из вашего <code>creators.json</code>. Авторы, которых вы добавили в 'избранное' (в данных JSON), отображаются вверху.</li>\n<li><b>Флажки:</b> Выберите одного или нескольких авторов, установив флажок рядом с их именем.</li>\n<li><b>Кнопка 'Область' (например, 'Область: Персонажи'):</b> Эта кнопка переключает организацию загрузки при запуске загрузок из этого всплывающего окна:\n<ul><li><i>Область: Персонажи:</i> Загрузки будут организованы в папки с именами персонажей непосредственно в вашем основном 'Месте для скачивания'. Работы разных авторов для одного и того же персонажа будут сгруппированы вместе.</li>\n<li><i>Область: Авторы:</i> Загрузки сначала создадут папку с именем автора в вашем основном 'Месте для скачивания'. Затем внутри папки каждого автора будут созданы подпапки с именами персонажей.</li></ul>\n</li>\n<li><b>Кнопка 'Добавить выбранные':</b> Нажатие этой кнопки возьмет имена всех отмеченных авторов и добавит их в основное поле ввода '🔗 URL автора/поста Kemono', разделенные запятыми. Затем диалоговое окно закроется.</li>\n</ul>\n</li>\n<li>Эта функция предоставляет быстрый способ заполнить поле URL для нескольких авторов без ручного ввода или вставки каждого URL.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step2_title":"② Фильтрация загрузок",
"help_guide_step2_content":"<html><head/><body>\n<h3>Фильтрация загрузок (левая панель)</h3>\n<ul>\n<li><b>🎯 Фильтровать по персонажу(ам):</b>\n<ul>\n<li>Введите имена через запятую (например, <code>Tifa, Aerith</code>).</li>\n<li><b>Сгруппированные псевдонимы для общей папки (отдельные записи в Known.txt):</b> <code>(Vivi, Ulti, Uta)</code>.\n<ul><li>Контент, соответствующий 'Vivi', 'Ulti' ИЛИ 'Uta', попадет в общую папку с названием 'Vivi Ulti Uta' (после очистки).</li>\n<li>Если эти имена новые, будет предложено добавить 'Vivi', 'Ulti' и 'Uta' как <i>отдельные индивидуальные записи</i> в <code>Known.txt</code>.</li>\n</ul>\n</li>\n<li><b>Сгруппированные псевдонимы для общей папки (одна запись в Known.txt):</b> <code>(Yuffie, Sonon)~</code> (обратите внимание на тильду <code>~</code>).\n<ul><li>Контент, соответствующий 'Yuffie' ИЛИ 'Sonon', попадет в общую папку с названием 'Yuffie Sonon'.</li>\n<li>Если новый, 'Yuffie Sonon' (с псевдонимами Yuffie, Sonon) будет предложено добавить как <i>одну групповую запись</i> в <code>Known.txt</code>.</li>\n</ul>\n</li>\n<li>Этот фильтр влияет на именование папок, если включена опция 'Раздельные папки по имени/заголовку'.</li>\n</ul>\n</li>\n<li><b>Фильтр: кнопка [Тип] (область фильтрации персонажей):</b> Переключает способ применения 'Фильтровать по персонажу(ам)':\n<ul>\n<li><code>Фильтр: Файлы</code>: Проверяет имена отдельных файлов. Пост сохраняется, если совпадает хотя бы один файл; скачиваются только совпадающие файлы. Именование папок использует персонажа из совпадающего имени файла.</li>\n<li><code>Фильтр: Заголовок</code>: Проверяет заголовки постов. Скачиваются все файлы из совпадающего поста. Именование папок использует персонажа из совпадающего заголовка поста.</li>\n<li><code>Фильтр: Оба</code>: Сначала проверяет заголовок поста. Если он совпадает, скачиваются все файлы. Если нет, то проверяет имена файлов, и скачиваются только совпадающие файлы. Именование папок отдает приоритет совпадению заголовка, затем совпадению файла.</li>\n<li><code>Фильтр: Комментарии (бета)</code>: Сначала проверяет имена файлов. Если файл совпадает, скачиваются все файлы из поста. Если совпадения по файлам нет, то проверяет комментарии к посту. Если комментарий совпадает, скачиваются все файлы. (Использует больше запросов к API). Именование папок отдает приоритет совпадению файла, затем совпадению комментария.</li>\n</ul>\n</li>\n<li><b>🗄️ Пользовательское имя папки (только для одного поста):</b>\n<ul>\n<li>Видно и доступно только при загрузке URL-адреса одного конкретного поста И когда включена опция 'Раздельные папки по имени/заголовку'.</li>\n<li>Позволяет указать пользовательское имя для папки загрузки этого одного поста.</li>\n</ul>\n</li>\n<li><b>🚫 Пропускать со словами:</b>\n<ul><li>Введите слова через запятую (например, <code>WIP, sketch, preview</code>), чтобы пропустить определенный контент.</li></ul>\n</li>\n<li><b>Область: кнопка [Тип] (область слов для пропуска):</b> Переключает способ применения 'Пропускать со словами':\n<ul>\n<li><code>Область: Файлы</code>: Пропускает отдельные файлы, если их имена содержат какие-либо из этих слов.</li>\n<li><code>Область: Посты</code>: Пропускает целые посты, если их заголовки содержат какие-либо из этих слов.</li>\n<li><code>Область: Оба</code>: Применяет оба (сначала заголовок поста, затем отдельные файлы).</li>\n</ul>\n</li>\n<li><b>✂️ Удалить слова из названия:</b>\n<ul><li>Введите слова через запятую (например, <code>patreon, [HD]</code>) для удаления из имен скачиваемых файлов (без учета регистра).</li></ul>\n</li>\n<li><b>Фильтровать файлы (радиокнопки):</b> Выберите, что скачивать:\n<ul>\n<li><code>Все</code>: Скачивает все найденные типы файлов.</li>\n<li><code>Изображения/GIF</code>: Только распространенные форматы изображений (JPG, PNG, GIF, WEBP и т. д.) и GIF.</li>\n<li><code>Видео</code>: Только распространенные форматы видео (MP4, MKV, WEBM, MOV и т. д.).</li>\n<li><code>📦 Только архивы</code>: Скачивает исключительно файлы <b>.zip</b> и <b>.rar</b>. При выборе этой опции флажки 'Пропускать .zip' и 'Пропускать .rar' автоматически отключаются и снимаются. 'Показывать внешние ссылки' также отключается.</li>\n<li><code>🎧 Только аудио</code>: Скачивает только распространенные аудиоформаты (MP3, WAV, FLAC, M4A, OGG и т. д.). Другие специфичные для файлов опции ведут себя так же, как в режиме 'Изображения' или 'Видео'.</li>\n<li><code>🔗 Только ссылки</code>: Извлекает и отображает внешние ссылки из описаний постов вместо скачивания файлов. Опции, связанные со скачиванием, и 'Показывать внешние ссылки' отключаются. Основная кнопка загрузки меняется на '🔗 Извлечь ссылки'.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step3_title":"③ Параметры и настройки загрузки",
"help_guide_step3_content":"<html><head/><body>\n<h3>Параметры и настройки загрузки (левая панель)</h3>\n<ul>\n<li><b>Пропускать .zip / Пропускать .rar:</b> Флажки для предотвращения загрузки этих типов архивных файлов. (Отключены и игнорируются, если выбран режим фильтра '📦 Только архивы').</li>\n<li><b>Скачивать только миниатюры:</b> Скачивает небольшие изображения предварительного просмотра вместо полноразмерных файлов (если доступны).</li>\n<li><b>Сжимать большие изображения (в WebP):</b> Если установлена библиотека 'Pillow' (PIL), изображения размером более 1,5 МБ будут преобразованы в формат WebP, если версия WebP значительно меньше.</li>\n<li><b>⚙️ Расширенные настройки:</b>\n<ul>\n<li><b>Раздельные папки по имени/заголовку:</b> Создает подпапки на основе ввода 'Фильтровать по персонажу(ам)' или заголовков постов. Может использовать список <b>Known.txt</b> в качестве запасного варианта для названий папок.</li></ul></li></ul></body></html>",
"help_guide_step4_title":"④ Расширенные настройки (Часть 1)",
"help_guide_step4_content":"<html><head/><body><h3>⚙️ Расширенные настройки (продолжение)</h3><ul><ul>\n<li><b>Подпапка для каждого поста:</b> Если опция 'Раздельные папки' включена, это создает дополнительную подпапку для <i>каждого отдельного поста</i> внутри основной папки персонажа/заголовка.</li>\n<li><b>Использовать cookie:</b> Установите этот флажок для использования файлов cookie для запросов.\n<ul>\n<li><b>Текстовое поле:</b> Введите строку cookie напрямую (например, <code>name1=value1; name2=value2</code>).</li>\n<li><b>Обзор...:</b> Выберите файл <code>cookies.txt</code> (формат Netscape). Путь появится в текстовом поле.</li>\n<li><b>Приоритет:</b> Текстовое поле (если заполнено) имеет приоритет над просматриваемым файлом. Если флажок 'Использовать cookie' установлен, но оба поля пусты, он попытается загрузить <code>cookies.txt</code> из каталога приложения.</li>\n</ul>\n</li>\n<li><b>Использовать многопоточность и ввод потоков:</b>\n<ul>\n<li>Включает более быстрые операции. Число в поле 'Потоки' означает:\n<ul>\n<li>Для <b>Лент авторов:</b> Количество постов для одновременной обработки. Файлы в каждом посте скачиваются последовательно его рабочим потоком (если не включено именование манги 'На основе даты', что принудительно использует 1 рабочий поток для поста).</li>\n<li>Для <b>URL отдельных постов:</b> Количество файлов для одновременной загрузки из этого одного поста.</li>\n</ul>\n</li>\n<li>Если флажок не установлен, используется 1 поток. Высокое количество потоков (например, >40) может показать предупреждение.</li>\n</ul>\n</li></ul></ul></body></html>",
"help_guide_step5_title":"⑤ Расширенные настройки (Часть 2) и действия",
"help_guide_step5_content":"<html><head/><body><h3>⚙️ Расширенные настройки (продолжение)</h3><ul><ul>\n<li><b>Показывать внешние ссылки в журнале:</b> Если отмечено, под основным журналом появится дополнительная панель журнала для отображения любых внешних ссылок, найденных в описаниях постов. (Отключено, если активен режим '🔗 Только ссылки' или '📦 Только архивы').</li>\n<li><b>📖 Режим манги/комиксов (только URL автора):</b> Специально для последовательного контента.\n<ul>\n<li>Скачивает посты от <b>самых старых к самым новым</b>.</li>\n<li>Поле 'Диапазон страниц' отключено, так как скачиваются все посты.</li>\n<li>Кнопка <b>переключения стиля имени файла</b> (например, 'Название: Заголовок поста') появляется в верхнем правом углу области журнала, когда этот режим активен для ленты автора. Нажмите ее, чтобы переключаться между стилями именования:\n<ul>\n<li><code>Название: Заголовок поста (по умолчанию)</code>: Первый файл в посте называется по очищенному заголовку поста (например, 'Моя глава 1.jpg'). Последующие файлы в *том же посте* попытаются сохранить свои исходные имена файлов (например, 'page_02.png', 'bonus_art.jpg'). Если в посте только один файл, он называется по заголовку поста. Это обычно рекомендуется для большинства манг/комиксов.</li>\n<li><code>Название: Исходный файл</code>: Все файлы пытаются сохранить свои исходные имена файлов.</li>\n<li><code>Название: Исходный файл</code>: Все файлы пытаются сохранить свои исходные имена файлов. Когда этот стиль активен, рядом с этой кнопкой стиля появится поле ввода для <b>необязательного префикса имени файла</b> (например, 'МояСерия_'). Пример: 'МояСерия_ИсходныйФайл.jpg'.</li>\n<li><code>Название: Заголовок+Г.ном. (Заголовок поста + Глобальная нумерация)</code>: Все файлы во всех постах текущей сессии скачивания именуются последовательно с использованием очищенного заголовка поста в качестве префикса, за которым следует глобальный счетчик. Пример: Пост 'Глава 1' (2 файла) -> 'Глава 1 001.jpg', 'Глава 1 002.png'. Следующий пост 'Глава 2' (1 файл) -> 'Глава 2 003.jpg'. Многопоточность для обработки постов автоматически отключается для этого стиля.</li>\n<li><code>Название: На основе даты</code>: Файлы именуются последовательно (001.ext, 002.ext, ...) на основе порядка публикации. Когда этот стиль активен, рядом с этой кнопкой стиля появится поле ввода для <b>необязательного префикса имени файла</b> (например, 'МояСерия_'). Пример: 'МояСерия_001.jpg'. Многопоточность для обработки постов автоматически отключается для этого стиля.</li>\n</ul>\n</li>\n<li>Для достижения наилучших результатов со стилями 'Название: Заголовок поста', 'Название: Заголовок+Г.ном.' или 'Название: На основе даты' используйте поле 'Фильтровать по персонажу(ам)' с названием манги/серии для организации папок.</li>\n</ul>\n</li>\n</ul></li></ul>\n<h3>Основные кнопки действий (левая панель)</h3>\n<ul>\n<li><b>⬇️ Начать скачивание / 🔗 Извлечь ссылки:</b> Текст и функция этой кнопки меняются в зависимости от выбора радиокнопки 'Фильтровать файлы'. Она запускает основную операцию.</li>\n<li><b>⏸️ Приостановить скачивание / ▶️ Возобновить скачивание:</b> Позволяет временно остановить текущий процесс скачивания/извлечения и возобновить его позже. Некоторые настройки интерфейса можно изменить во время паузы.</li>\n<li><b>❌ Отменить и сбросить интерфейс:</b> Останавливает текущую операцию и выполняет мягкий сброс интерфейса. Ваши вводы URL и каталога загрузки сохраняются, но другие настройки и журналы очищаются.</li>\n</ul></body></html>",
"help_guide_step6_title":"⑥ Список известных шоу/персонажей",
"help_guide_step6_content":"<html><head/><body>\n<h3>Управление списком известных шоу/персонажей (внизу слева)</h3>\n<p>Этот раздел помогает управлять файлом <code>Known.txt</code>, который используется для умной организации папок, когда включена опция 'Раздельные папки по имени/заголовку', особенно в качестве запасного варианта, если пост не соответствует вашему активному вводу 'Фильтровать по персонажу(ам)'.</p>\n<ul>\n<li><b>Открыть Known.txt:</b> Открывает файл <code>Known.txt</code> (расположенный в каталоге приложения) в вашем текстовом редакторе по умолчанию для расширенного редактирования (например, создания сложных сгруппированных псевдонимов).</li>\n<li><b>Поиск персонажей...:</b> Фильтрует список известных имен, отображаемый ниже.</li>\n<li><b>Виджет списка:</b> Отображает основные имена из вашего <code>Known.txt</code>. Выберите здесь записи для их удаления.</li>\n<li><b>Добавить новое название шоу/персонажа (поле ввода):</b> Введите имя или группу для добавления.\n<ul>\n<li><b>Простое имя:</b> например, <code>Моя потрясающая серия</code>. Добавляется как одна запись.</li>\n<li><b>Группа для отдельных записей в Known.txt:</b> например, <code>(Vivi, Ulti, Uta)</code>. Добавляет 'Vivi', 'Ulti' и 'Uta' как три отдельные индивидуальные записи в <code>Known.txt</code>.</li>\n<li><b>Группа для общей папки и одной записи в Known.txt (тильда <code>~</code>):</b> например, <code>(Персонаж А, Перс А)~</code>. Добавляет одну запись в <code>Known.txt</code> с названием 'Персонаж А Перс А'. 'Персонаж А' и 'Перс А' становятся псевдонимами для этой одной папки/записи.</li>\n</ul>\n</li>\n<li><b>➕ Кнопка 'Добавить':</b> Добавляет имя/группу из поля ввода выше в список и <code>Known.txt</code>.</li>\n<li><b>⤵️ Кнопка 'Добавить в фильтр':</b>\n<ul>\n<li>Расположена рядом с кнопкой '➕ Добавить' для списка 'Известные шоу/персонажи'.</li>\n<li>Нажатие этой кнопки открывает всплывающее окно со списком всех имен из вашего файла <code>Known.txt</code>, каждое с флажком.</li>\n<li>Всплывающее окно включает панель поиска для быстрой фильтрации списка имен.</li>\n<li>Вы можете выбрать одно или несколько имен, используя флажки.</li>\n<li>Нажмите 'Добавить выбранные', чтобы вставить выбранные имена в поле ввода 'Фильтровать по персонажу(ам)' в главном окне.</li>\n<li>Если выбранное имя из <code>Known.txt</code> изначально было группой (например, определено как <code>(Boa, Hancock)</code> в Known.txt), оно будет добавлено в поле фильтра как <code>(Boa, Hancock)~</code>. Простые имена добавляются как есть.</li>\n<li>Для удобства во всплывающем окне доступны кнопки 'Выбрать все' и 'Снять выделение со всех'.</li>\n<li>Нажмите 'Отмена', чтобы закрыть всплывающее окно без каких-либо изменений.</li>\n</ul>\n</li>\n<li><b>🗑️ Кнопка 'Удалить выбранные':</b> Удаляет выбранные имена из списка и <code>Known.txt</code>.</li>\n<li><b>❓ Кнопка (именно эта!):</b> Отображает это подробное руководство по помощи.</li>\n</ul></body></html>",
"help_guide_step7_title":"⑦ Область журнала и элементы управления",
"help_guide_step7_content":"<html><head/><body>\n<h3>Область журнала и элементы управления (правая панель)</h3>\n<ul>\n<li><b>📜 Журнал прогресса / Журнал извлеченных ссылок (метка):</b> Заголовок для основной области журнала; меняется, если активен режим '🔗 Только ссылки'.</li>\n<li><b>Поиск ссылок... / 🔍 Кнопка (поиск ссылок):</b>\n<ul><li>Видно только тогда, когда активен режим '🔗 Только ссылки'. Позволяет в реальном времени фильтровать извлеченные ссылки, отображаемые в основном журнале, по тексту, URL или платформе.</li></ul>\n</li>\n<li><b>Название: кнопка [Стиль] (стиль имени файла манги):</b>\n<ul><li>Видно только тогда, когда активен <b>Режим манги/комиксов</b> для ленты автора и не в режиме 'Только ссылки' или 'Только архивы'.</li>\n<li>Переключает стили имен файлов: <code>Заголовок поста</code>, <code>Исходный файл</code>, <code>На основе даты</code>. (Подробности см. в разделе 'Режим манги/комиксов').</li>\n<li>Когда активен стиль 'Исходный файл' или 'На основе даты', рядом с этой кнопкой появится поле ввода для <b>необязательного префикса имени файла</b>.</li>\n</ul>\n</li>\n<li><b>Многочаст.: кнопка [ВКЛ/ВЫКЛ]:</b>\n<ul><li>Переключает многосегментную загрузку для отдельных больших файлов.\n<ul><li><b>ВКЛ:</b> Может ускорить загрузку больших файлов (например, видео), но может увеличить 'дерганье' интерфейса или спам в журнале при большом количестве мелких файлов. При включении появляется предупреждение. Если многочастная загрузка не удалась, она повторяется в однопоточном режиме.</li>\n<li><b>ВЫКЛ (по умолчанию):</b> Файлы скачиваются одним потоком.</li>\n</ul>\n<li>Отключено, если активен режим '🔗 Только ссылки' или '📦 Только архивы'.</li>\n</ul>\n</li>\n<li><b>👁️ / 🙈 Кнопка (переключатель вида журнала):</b> Переключает вид основного журнала:\n<ul>\n<li><b>👁️ Журнал прогресса (по умолчанию):</b> Показывает всю активность загрузки, ошибки и сводки.</li>\n<li><b>🙈 Журнал пропущенных персонажей:</b> Отображает список ключевых терминов из заголовков/содержимого постов, которые были пропущены из-за ваших настроек 'Фильтровать по персонажу(ам)'. Полезно для выявления контента, который вы можете непреднамеренно пропускать.</li>\n</ul>\n</li>\n<li><b>🔄 Кнопка 'Сброс':</b> Очищает все поля ввода, журналы и сбрасывает временные настройки до их значений по умолчанию. Может использоваться только тогда, когда загрузка не активна.</li>\n<li><b>Основной вывод журнала (текстовая область):</b> Отображает подробные сообщения о ходе выполнения, ошибки и сводки. Если активен режим '🔗 Только ссылки', эта область отображает извлеченные ссылки.</li>\n<li><b>Вывод журнала пропущенных персонажей (текстовая область):</b> (Просматривается с помощью переключателя 👁️ / 🙈) Отображает посты/файлы, пропущенные из-за фильтров персонажей.</li>\n<li><b>Вывод внешнего журнала (текстовая область):</b> Появляется под основным журналом, если отмечен флажок 'Показывать внешние ссылки в журнале'. Отображает внешние ссылки, найденные в описаниях постов.</li>\n<li><b>Кнопка 'Экспортировать ссылки':</b>\n<ul><li>Видно и доступно только тогда, когда активен режим '🔗 Только ссылки' и были извлечены ссылки.</li>\n<li>Позволяет сохранить все извлеченные ссылки в файл <code>.txt</code>.</li>\n</ul>\n</li>\n<li><b>Прогресс: метка [Статус]:</b> Показывает общий ход процесса скачивания или извлечения ссылок (например, обработанные посты).</li>\n<li><b>Метка прогресса файла:</b> Показывает ход скачивания отдельных файлов, включая скорость и размер, или статус многочастной загрузки.</li>\n</ul></body></html>",
"help_guide_step8_title":"⑧ Режим избранного и будущие функции",
"help_guide_step8_content":"<html><head/><body>\n<h3>Режим избранного (скачивание из ваших избранных на Kemono.su)</h3>\n<p>Этот режим позволяет скачивать контент непосредственно от художников, которых вы добавили в избранное на Kemono.su.</p>\n<ul>\n<li><b>⭐ Как включить:</b>\n<ul>\n<li>Установите флажок <b>'⭐ Режим избранного'</b>, расположенный рядом с радиокнопкой '🔗 Только ссылки'.</li>\n</ul>\n</li>\n<li><b>Изменения интерфейса в режиме избранного:</b>\n<ul>\n<li>Область ввода '🔗 URL автора/поста Kemono' заменяется сообщением о том, что режим избранного активен.</li>\n<li>Стандартные кнопки 'Начать скачивание', 'Пауза', 'Отмена' заменяются на:\n<ul>\n<li>Кнопка <b>'🖼️ Избранные художники'</b></li>\n<li>Кнопка <b>'📄 Избранные посты'</b></li>\n</ul>\n</li>\n<li>Опция '🍪 Использовать cookie' автоматически включается и блокируется, так как для загрузки избранного требуются файлы cookie.</li>\n</ul>\n</li>\n<li><b>🖼️ Кнопка 'Избранные художники':</b>\n<ul>\n<li>Нажатие этой кнопки открывает диалоговое окно со списком всех художников, которых вы добавили в избранное на Kemono.su.</li>\n<li>Вы можете выбрать одного или нескольких художников из этого списка для скачивания их контента.</li>\n</ul>\n</li>\n<li><b>📄 Кнопка 'Избранные посты' (будущая функция):</b>\n<ul>\n<li>Скачивание конкретных избранных <i>постов</i> (особенно в последовательном порядке, как манга, если они являются частью серии) — это функция, которая в настоящее время находится в разработке.</li>\n<li>Лучший способ обработки избранных постов, особенно для последовательного чтения, как манга, все еще изучается.</li>\n<li>Если у вас есть конкретные идеи или варианты использования того, как вы хотели бы скачивать и организовывать избранные посты (например, 'в стиле манги' из избранного), пожалуйста, рассмотрите возможность открыть issue или присоединиться к обсуждению на странице проекта на GitHub. Ваш вклад очень ценен!</li>\n</ul>\n</li>\n<li><b>Область скачивания избранного (кнопка):</b>\n<ul>\n<li>Эта кнопка (рядом с 'Избранными постами') управляет тем, куда скачивается контент от выбранных избранных художников:\n<ul>\n<li><b><i>Область: Выбранное место:</i></b> Все выбранные художники скачиваются в основное 'Место для скачивания', которое вы установили в интерфейсе. Фильтры применяются глобально ко всему контенту.</li>\n<li><b><i>Область: Папки художников:</i></b> Для каждого выбранного художника в вашем основном 'Месте для скачивания' автоматически создается подпапка (с именем художника). Контент этого художника попадает в их конкретную подпапку. Фильтры применяются внутри выделенной папки каждого художника.</li>\n</ul>\n</li>\n</ul>\n</li>\n<li><b>Фильтры в режиме избранного:</b>\n<ul>\n<li>Опции '🎯 Фильтровать по персонажу(ам)', '🚫 Пропускать со словами' и 'Фильтровать файлы', которые вы установили в интерфейсе, по-прежнему будут применяться к контенту, скачиваемому от ваших избранных художников.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step9_title":"⑨ Ключевые файлы и руководство",
"help_guide_step9_content":"<html><head/><body>\n<h3>Ключевые файлы, используемые приложением</h3>\n<ul>\n<li><b><code>Known.txt</code>:</b>\n<ul>\n<li>Находится в каталоге приложения (там же, где <code>.exe</code> или <code>main.py</code>).</li>\n<li>Хранит ваш список известных шоу, персонажей или названий серий для автоматической организации папок, когда включена опция 'Раздельные папки по имени/заголовку'.</li>\n<li><b>Формат:</b>\n<ul>\n<li>Каждая строка - это запись.</li>\n<li><b>Простое имя:</b> например, <code>Моя потрясающая серия</code>. Контент, соответствующий этому, попадет в папку с названием 'Моя потрясающая серия'.</li>\n<li><b>Сгруппированные псевдонимы:</b> например, <code>(Персонаж А, Перс А, Альтернативное имя А)</code>. Контент, соответствующий 'Персонаж А', 'Перс А' ИЛИ 'Альтернативное имя А', попадет в ОДНУ папку с названием 'Персонаж А Перс А Альтернативное имя А' (после очистки). Все термины в скобках становятся псевдонимами для этой папки.</li>\n</ul>\n</li>\n<li><b>Использование:</b> Служит запасным вариантом для именования папок, если пост не соответствует вашему активному вводу 'Фильтровать по персонажу(ам)'. Вы можете управлять простыми записями через интерфейс или редактировать файл напрямую для сложных псевдонимов. Приложение перезагружает его при запуске или следующем использовании.</li>\n</ul>\n</li>\n<li><b><code>cookies.txt</code> (необязательно):</b>\n<ul>\n<li>Если вы используете функцию 'Использовать cookie' и не предоставляете прямую строку cookie или не просматриваете конкретный файл, приложение будет искать файл с именем <code>cookies.txt</code> в своем каталоге.</li>\n<li><b>Формат:</b> Должен быть в формате файла cookie Netscape.</li>\n<li><b>Использование:</b> Позволяет загрузчику использовать сеанс входа в ваш браузер для доступа к контенту, который может быть заблокирован на Kemono/Coomer.</li>\n</ul>\n</li>\n</ul>\n<h3>Руководство для первого пользователя</h3>\n<ul>\n<li>При первом запуске (или при сбросе) появляется диалоговое окно приветственного руководства, которое проведет вас по основным функциям. Вы можете пропустить его или выбрать 'Больше не показывать это руководство'.</li>\n</ul>\n<p><em>Многие элементы интерфейса также имеют всплывающие подсказки, которые появляются при наведении на них курсора мыши, предоставляя быстрые подсказки.</em></p>\n</body></html>"
})

translations ["ko"]={}
translations ["ko"].update ({
"settings_dialog_title":"설정",
"language_label":"언어:",
"lang_english":"영어 (English)",
"lang_japanese":"일본어 (日本語)",
"theme_toggle_light":"라이트 모드로 전환",
"theme_toggle_dark":"다크 모드로 전환",
"theme_tooltip_light":"애플리케이션 모양을 라이트 모드로 변경합니다.",
"theme_tooltip_dark":"애플리케이션 모양을 다크 모드로 변경합니다.",
"ok_button":"확인",
"appearance_group_title":"모양",
"language_group_title":"언어 설정",
"creator_post_url_label":"🔗 Kemono 작가/게시물 URL:",
"download_location_label":"📁 다운로드 위치:",
"filter_by_character_label":"🎯 캐릭터로 필터링 (쉼표로 구분):",
"skip_with_words_label":"🚫 단어로 건너뛰기 (쉼표로 구분):",
"remove_words_from_name_label":"✂️ 이름에서 단어 제거:",
"filter_all_radio":"전체",
"filter_images_radio":"이미지/GIF",
"filter_videos_radio":"비디오",
"filter_archives_radio":"📦 아카이브만",
"filter_links_radio":"🔗 링크만",
"filter_audio_radio":"� 오디오만",
"favorite_mode_checkbox_label":"⭐ 즐겨찾기 모드",
"browse_button_text":"찾아보기...",
"char_filter_scope_files_text":"필터: 파일",
"char_filter_scope_files_tooltip":"현재 범위: 파일\n\n이름으로 개별 파일을 필터링합니다. 파일이 하나라도 일치하면 게시물이 유지됩니다.\n해당 게시물에서 일치하는 파일만 다운로드됩니다.\n예: 필터 'Tifa'. 'Tifa_artwork.jpg' 파일이 일치하여 다운로드됩니다.\n폴더 이름 지정: 일치하는 파일 이름의 캐릭터를 사용합니다.\n\n클릭하여 다음으로 전환: 둘 다",
"char_filter_scope_title_text":"필터: 제목",
"char_filter_scope_title_tooltip":"현재 범위: 제목\n\n제목으로 전체 게시물을 필터링합니다. 일치하는 게시물의 모든 파일이 다운로드됩니다.\n예: 필터 'Aerith'. 'Aerith's Garden'이라는 제목의 게시물이 일치하여 모든 파일이 다운로드됩니다.\n폴더 이름 지정: 일치하는 게시물 제목의 캐릭터를 사용합니다.\n\n클릭하여 다음으로 전환: 파일",
"char_filter_scope_both_text":"필터: 둘 다",
"char_filter_scope_both_tooltip":"현재 범위: 둘 다 (제목 우선, 그 다음 파일)\n\n1. 게시물 제목을 확인합니다: 일치하면 게시물의 모든 파일이 다운로드됩니다.\n2. 제목이 일치하지 않으면 파일 이름을 확인합니다: 파일이 일치하면 해당 파일만 다운로드됩니다.\n예: 필터 'Cloud'.\n - 'Cloud Strife' 게시물 (제목 일치) -> 모든 파일 다운로드.\n - 'Bike Chase' 게시물에 'Cloud_fenrir.jpg' 파일 (파일 일치) -> 'Cloud_fenrir.jpg'만 다운로드.\n폴더 이름 지정: 제목 일치를 우선으로 하고, 그 다음 파일 일치를 따릅니다.\n\n클릭하여 다음으로 전환: 댓글",
"char_filter_scope_comments_text":"필터: 댓글 (베타)",
"char_filter_scope_comments_tooltip":"현재 범위: 댓글 (베타 - 파일 우선, 그 다음 댓글을 예비로 사용)\n\n1. 파일 이름을 확인합니다: 게시물의 파일이 필터와 일치하면 전체 게시물이 다운로드됩니다. 이 필터 용어에 대해 댓글은 확인되지 않습니다.\n2. 파일이 일치하지 않으면 게시물 댓글을 확인합니다: 댓글이 일치하면 전체 게시물이 다운로드됩니다.\n예: 필터 'Barret'.\n - 게시물 A: 파일 'Barret_gunarm.jpg', 'other.png'. 'Barret_gunarm.jpg' 파일 일치. 게시물 A의 모든 파일 다운로드. 'Barret'에 대한 댓글은 확인되지 않음.\n - 게시물 B: 파일 'dyne.jpg', 'weapon.gif'. 댓글: '...Barret Wallace의 그림...'. 'Barret'에 대한 파일 일치 없음. 댓글 일치. 게시물 B의 모든 파일 다운로드.\n폴더 이름 지정: 파일 일치의 캐릭터를 우선으로 하고, 그 다음 댓글 일치의 캐릭터를 따릅니다.\n\n클릭하여 다음으로 전환: 제목",
"char_filter_scope_unknown_text":"필터: 알 수 없음",
"char_filter_scope_unknown_tooltip":"현재 범위: 알 수 없음\n\n캐릭터 필터 범위가 알 수 없는 상태입니다. 순환하거나 재설정하십시오.\n\n클릭하여 다음으로 전환: 제목",
"skip_words_input_tooltip":"쉼표로 구분된 단어를 입력하여 특정 콘텐츠(예: WIP, 스케치, 미리보기)의 다운로드를 건너뜁니다.\n\n이 입력 옆에 있는 '범위: [유형]' 버튼은 이 필터가 적용되는 방식을 순환합니다:\n- 범위: 파일: 파일 이름에 이 단어 중 하나라도 포함되어 있으면 개별 파일을 건너뜁니다.\n- 범위: 게시물: 게시물 제목에 이 단어 중 하나라도 포함되어 있으면 전체 게시물을 건너뜁니다.\n- 범위: 둘 다: 둘 다 적용합니다 (게시물 제목이 먼저, 게시물 제목이 괜찮으면 개별 파일).",
"remove_words_input_tooltip":"다운로드한 파일 이름에서 제거할 단어를 쉼표로 구분하여 입력합니다(대소문자 구분 없음).\n일반적인 접두사/접미사를 정리하는 데 유용합니다.\n예: patreon, kemono, [HD], _final",
"skip_scope_files_text":"범위: 파일",
"skip_scope_files_tooltip":"현재 건너뛰기 범위: 파일\n\n파일 이름에 '건너뛸 단어'가 포함되어 있으면 개별 파일을 건너뜁니다.\n예: 건너뛸 단어 \"WIP, sketch\".\n- 파일 \"art_WIP.jpg\" -> 건너뜀.\n- 파일 \"final_art.png\" -> 다운로드됨 (다른 조건이 충족될 경우).\n\n게시물은 다른 건너뛰지 않은 파일에 대해 계속 처리됩니다.\n클릭하여 다음으로 전환: 둘 다",
"skip_scope_posts_text":"범위: 게시물",
"skip_scope_posts_tooltip":"현재 건너뛰기 범위: 게시물\n\n게시물 제목에 '건너뛸 단어'가 포함되어 있으면 전체 게시물을 건너뜁니다.\n건너뛴 게시물의 모든 파일은 무시됩니다.\n예: 건너뛸 단어 \"preview, announcement\".\n- 게시물 \"흥미로운 발표!\" -> 건너뜀.\n- 게시물 \"완성된 작품\" -> 처리됨 (다른 조건이 충족될 경우).\n\n클릭하여 다음으로 전환: 파일",
"skip_scope_both_text":"범위: 둘 다",
"skip_scope_both_tooltip":"현재 건너뛰기 범위: 둘 다 (게시물 우선, 그 다음 파일)\n\n1. 게시물 제목을 확인합니다: 제목에 건너뛸 단어가 포함되어 있으면 전체 게시물을 건너뜁니다.\n2. 게시물 제목이 괜찮으면 개별 파일 이름을 확인합니다: 파일 이름에 건너뛸 단어가 포함되어 있으면 해당 파일만 건너뜁니다.\n예: 건너뛸 단어 \"WIP, sketch\".\n- 게시물 \"스케치 및 WIP\" (제목 일치) -> 전체 게시물 건너뜀.\n- 게시물 \"아트 업데이트\" (제목 괜찮음)와 파일:\n  - \"character_WIP.jpg\" (파일 일치) -> 건너뜀.\n  - \"final_scene.png\" (파일 괜찮음) -> 다운로드됨.\n\n클릭하여 다음으로 전환: 게시물",
"skip_scope_unknown_text":"범위: 알 수 없음",
"skip_scope_unknown_tooltip":"현재 건너뛰기 범위가 알 수 없는 상태입니다. 순환하거나 재설정하십시오.\n\n클릭하여 다음으로 전환: 게시물",
"language_change_title":"언어 변경됨",
"language_change_message":"언어가 변경되었습니다. 모든 변경 사항이 완전히 적용되려면 다시 시작해야 합니다.",
"language_change_informative":"지금 애플리케이션을 다시 시작하시겠습니까?",
"restart_now_button":"지금 다시 시작",
"skip_zip_checkbox_label":".zip 건너뛰기",
"skip_rar_checkbox_label":".rar 건너뛰기",
"download_thumbnails_checkbox_label":"썸네일만 다운로드",
"scan_content_images_checkbox_label":"이미지 콘텐츠 스캔",
"compress_images_checkbox_label":"WebP로 압축",
"separate_folders_checkbox_label":"이름/제목별로 폴더 분리",
"subfolder_per_post_checkbox_label":"게시물당 하위 폴더",
"use_cookie_checkbox_label":"쿠키 사용",
"use_multithreading_checkbox_base_label":"멀티스레딩 사용",
"show_external_links_checkbox_label":"로그에 외부 링크 표시",
"manga_comic_mode_checkbox_label":"만화/코믹 모드",
"threads_label":"스레드:",
"start_download_button_text":"⬇️ 다운로드 시작",
"start_download_button_tooltip":"현재 설정으로 다운로드 또는 링크 추출 프로세스를 시작하려면 클릭하십시오.",
"extract_links_button_text":"🔗 링크 추출",
"pause_download_button_text":"⏸️ 다운로드 일시 중지",
"pause_download_button_tooltip":"진행 중인 다운로드 프로세스를 일시 중지하려면 클릭하십시오.",
"resume_download_button_text":"▶️ 다운로드 재개",
"resume_download_button_tooltip":"다운로드를 재개하려면 클릭하십시오.",
"cancel_button_text":"❌ 취소 및 UI 재설정",
"cancel_button_tooltip":"진행 중인 다운로드/추출 프로세스를 취소하고 UI 필드를 재설정하려면 클릭하십시오(URL 및 디렉토리 보존).",
"error_button_text":"오류",
"error_button_tooltip":"오류로 인해 건너뛴 파일을 보고 선택적으로 다시 시도하십시오.",
"cancel_retry_button_text":"❌ 재시도 취소",
"known_chars_label_text":"🎭 알려진 프로그램/캐릭터 (폴더 이름용):",
"open_known_txt_button_text":"Known.txt 열기",
"known_chars_list_tooltip":"이 목록에는 '폴더 분리'가 켜져 있고 특정 '캐릭터로 필터링'이 제공되지 않거나 게시물과 일치하지 않을 때 자동 폴더 생성에 사용되는 이름이 포함되어 있습니다.\n자주 다운로드하는 시리즈, 게임 또는 캐릭터의 이름을 추가하십시오.",
"open_known_txt_button_tooltip":"기본 텍스트 편집기에서 'Known.txt' 파일을 엽니다.\n파일은 애플리케이션 디렉토리에 있습니다.",
"add_char_button_text":"➕ 추가",
"add_char_button_tooltip":"입력 필드의 이름을 '알려진 프로그램/캐릭터' 목록에 추가합니다.",
"add_to_filter_button_text":"⤵️ 필터에 추가",
"add_to_filter_button_tooltip":"'알려진 프로그램/캐릭터' 목록에서 이름을 선택하여 위의 '캐릭터로 필터링' 필드에 추가합니다.",
"delete_char_button_text":"🗑️ 선택 항목 삭제",
"delete_char_button_tooltip":"'알려진 프로그램/캐릭터' 목록에서 선택한 이름을 삭제합니다.",
"progress_log_label_text":"📜 진행률 로그:",
"radio_all_tooltip":"게시물에서 찾은 모든 파일 유형을 다운로드합니다.",
"radio_images_tooltip":"일반적인 이미지 형식(JPG, PNG, GIF, WEBP 등)만 다운로드합니다.",
"radio_videos_tooltip":"일반적인 비디오 형식(MP4, MKV, WEBM, MOV 등)만 다운로드합니다.",
"radio_only_archives_tooltip":".zip 및 .rar 파일만 독점적으로 다운로드합니다. 다른 파일 관련 옵션은 비활성화됩니다.",
"radio_only_audio_tooltip":"일반적인 오디오 형식(MP3, WAV, FLAC 등)만 다운로드합니다.",
"radio_only_links_tooltip":"파일을 다운로드하는 대신 게시물 설명에서 외부 링크를 추출하여 표시합니다.\n다운로드 관련 옵션은 비활성화됩니다.",
"favorite_mode_checkbox_tooltip":"저장된 아티스트/게시물을 탐색하려면 즐겨찾기 모드를 활성화하십시오.\n이렇게 하면 URL 입력이 즐겨찾기 선택 버튼으로 대체됩니다.",
"skip_zip_checkbox_tooltip":"선택하면 .zip 아카이브 파일이 다운로드되지 않습니다.\n('아카이브만'을 선택하면 비활성화됨).",
"skip_rar_checkbox_tooltip":"선택하면 .rar 아카이브 파일이 다운로드되지 않습니다.\n('아카이브만'을 선택하면 비활성화됨).",
"download_thumbnails_checkbox_tooltip":"전체 크기 파일 대신 API에서 작은 미리보기 이미지를 다운로드합니다(사용 가능한 경우).\n'이미지 URL에 대한 게시물 콘텐츠 스캔'도 선택하면 이 모드는 콘텐츠 스캔에서 찾은 이미지만 다운로드합니다(API 썸네일 무시).",
"scan_content_images_checkbox_tooltip":"선택하면 다운로더가 게시물의 HTML 콘텐츠에서 이미지 URL(<img> 태그 또는 직접 링크에서)을 스캔합니다.\n여기에는 <img> 태그의 상대 경로를 전체 URL로 확인하는 것이 포함됩니다.\n<img> 태그의 상대 경로(예: /data/image.jpg)는 전체 URL로 확인됩니다.\n이미지가 게시물 설명에 있지만 API의 파일/첨부 파일 목록에 없는 경우에 유용합니다.",
"compress_images_checkbox_tooltip":"1.5MB보다 큰 이미지를 WebP 형식으로 압축합니다(Pillow 필요).",
"use_subfolders_checkbox_tooltip":"'캐릭터로 필터링' 입력 또는 게시물 제목을 기반으로 하위 폴더를 만듭니다.\n특정 필터가 일치하지 않으면 '알려진 프로그램/캐릭터' 목록을 폴더 이름의 대체 수단으로 사용합니다.\n단일 게시물에 대해 '캐릭터로 필터링' 입력 및 '사용자 지정 폴더 이름'을 활성화합니다.",
"use_subfolder_per_post_checkbox_tooltip":"각 게시물에 대한 하위 폴더를 만듭니다. '폴더 분리'도 켜져 있으면 캐릭터/제목 폴더 안에 있습니다.",
"use_cookie_checkbox_tooltip":"선택하면 요청에 애플리케이션 디렉토리의 'cookies.txt'(Netscape 형식)에서 쿠키를 사용하려고 시도합니다.\nKemono/Coomer에서 로그인해야 하는 콘텐츠에 액세스하는 데 유용합니다.",
"cookie_text_input_tooltip":"쿠키 문자열을 직접 입력하십시오.\n'쿠키 사용'이 선택되어 있고 'cookies.txt'를 찾을 수 없거나 이 필드가 비어 있지 않은 경우 사용됩니다.\n형식은 백엔드가 구문 분석하는 방식에 따라 다릅니다(예: 'name1=value1; name2=value2').",
"use_multithreading_checkbox_tooltip":"동시 작업을 활성화합니다. 자세한 내용은 '스레드' 입력을 참조하십시오.",
"thread_count_input_tooltip":"동시 작업 수.\n- 단일 게시물: 동시 파일 다운로드 (1-10 권장).\n- 작성자 피드 URL: 동시에 처리할 게시물 수 (1-200 권장).\n  각 게시물 내의 파일은 해당 작업자에 의해 하나씩 다운로드됩니다.\n'멀티스레딩 사용'을 선택하지 않으면 1개의 스레드가 사용됩니다.",
"external_links_checkbox_tooltip":"선택하면 주 로그 패널 아래에 보조 로그 패널이 나타나 게시물 설명에서 찾은 외부 링크를 표시합니다.\n('링크만' 또는 '아카이브만' 모드가 활성화된 경우 비활성화됨).",
"manga_mode_checkbox_tooltip":"게시물을 가장 오래된 것부터 최신 것까지 다운로드하고 게시물 제목에 따라 파일 이름을 바꿉니다(작성자 피드 전용).",
"multipart_on_button_text":"다중 파트: 켬",
"multipart_on_button_tooltip":"다중 파트 다운로드: 켬\n\n여러 세그먼트로 대용량 파일을 동시에 다운로드할 수 있습니다.\n- 단일 대용량 파일(예: 비디오)의 다운로드 속도를 높일 수 있습니다.\n- CPU/네트워크 사용량이 증가할 수 있습니다.\n- 파일이 많은 피드의 경우 속도 이점이 없을 수 있으며 UI/로그가 복잡해질 수 있습니다.\n- 다중 파트가 실패하면 단일 스트림으로 다시 시도합니다.\n\n클릭하여 끄기.",
"multipart_off_button_text":"다중 파트: 끔",
"multipart_off_button_tooltip":"다중 파트 다운로드: 끔\n\n모든 파일은 단일 스트림을 사용하여 다운로드됩니다.\n- 안정적이며 대부분의 시나리오, 특히 많은 작은 파일에 적합합니다.\n- 대용량 파일은 순차적으로 다운로드됩니다.\n\n클릭하여 켜기(권장 사항 참조).",
"reset_button_text":"🔄 재설정",
"reset_button_tooltip":"모든 입력 및 로그를 기본 상태로 재설정합니다(유휴 상태일 때만).",
"progress_idle_text":"진행률: 유휴",
"missed_character_log_label_text":"🚫 누락된 캐릭터 로그:",
"creator_popup_title":"작성자 선택",
"creator_popup_search_placeholder":"이름, 서비스로 검색하거나 작성자 URL을 붙여넣으십시오...",
"creator_popup_add_selected_button":"선택 항목 추가",
"creator_popup_scope_characters_button":"범위: 캐릭터",
"creator_popup_scope_creators_button":"범위: 작성자",
"favorite_artists_button_text":"🖼️ 즐겨찾는 아티스트",
"favorite_artists_button_tooltip":"Kemono.su/Coomer.su에서 즐겨찾는 아티스트를 탐색하고 다운로드하십시오.",
"favorite_posts_button_text":"📄 즐겨찾는 게시물",
"favorite_posts_button_tooltip":"Kemono.su/Coomer.su에서 즐겨찾는 게시물을 탐색하고 다운로드하십시오.",
"favorite_scope_selected_location_text":"범위: 선택한 위치",
"favorite_scope_selected_location_tooltip":"현재 즐겨찾기 다운로드 범위: 선택한 위치\n\n선택한 모든 즐겨찾는 아티스트/게시물은 UI에 지정된 기본 '다운로드 위치'에 다운로드됩니다.\n필터(캐릭터, 건너뛸 단어, 파일 유형)는 모든 콘텐츠에 전역적으로 적용됩니다.\n\n클릭하여 다음으로 변경: 아티스트 폴더",
"favorite_scope_artist_folders_text":"범위: 아티스트 폴더",
"favorite_scope_artist_folders_tooltip":"현재 즐겨찾기 다운로드 범위: 아티스트 폴더\n\n선택한 각 즐겨찾는 아티스트/게시물에 대해 기본 '다운로드 위치' 내에 새 하위 폴더(아티스트 이름)가 생성됩니다.\n해당 아티스트/게시물의 콘텐츠는 특정 하위 폴더에 다운로드됩니다.\n필터(캐릭터, 건너뛸 단어, 파일 유형)는 각 아티스트의 폴더 *내에서* 적용됩니다.\n\n클릭하여 다음으로 변경: 선택한 위치",
"favorite_scope_unknown_text":"범위: 알 수 없음",
"favorite_scope_unknown_tooltip":"즐겨찾기 다운로드 범위가 알 수 없습니다. 클릭하여 순환하십시오.",
"manga_style_post_title_text":"이름: 게시물 제목",
"manga_style_original_file_text":"이름: 원본 파일",
"manga_style_date_based_text":"이름: 날짜 기반",
"manga_style_title_global_num_text":"이름: 제목+전역 번호",
"manga_style_unknown_text":"이름: 알 수 없는 스타일",
"fav_artists_dialog_title":"즐겨찾는 아티스트",
"fav_artists_loading_status":"즐겨찾는 아티스트 로드 중...",
"fav_artists_search_placeholder":"아티스트 검색...",
"fav_artists_select_all_button":"모두 선택",
"fav_artists_deselect_all_button":"모두 선택 해제",
"fav_artists_download_selected_button":"선택 항목 다운로드",
"fav_artists_cancel_button":"취소",
"fav_artists_loading_from_source_status":"⏳ {source_name}에서 즐겨찾기 로드 중...",
"fav_artists_found_status":"총 {count}명의 즐겨찾는 아티스트를 찾았습니다.",
"fav_artists_none_found_status":"Kemono.su 또는 Coomer.su에서 즐겨찾는 아티스트를 찾을 수 없습니다.",
"fav_artists_failed_status":"즐겨찾기를 가져오는 데 실패했습니다.",
"fav_artists_cookies_required_status":"오류: 쿠키가 활성화되었지만 어떤 소스에 대해서도 로드할 수 없습니다.",
"fav_artists_no_favorites_after_processing":"처리 후 즐겨찾는 아티스트를 찾을 수 없습니다.",
"fav_artists_no_selection_title":"선택 항목 없음",
"fav_artists_no_selection_message":"다운로드할 아티스트를 하나 이상 선택하십시오.",
"fav_posts_dialog_title":"즐겨찾는 게시물",
"fav_posts_loading_status":"즐겨찾는 게시물 로드 중...",
"fav_posts_search_placeholder":"게시물 검색 (제목, 작성자, ID, 서비스)...",
"fav_posts_select_all_button":"모두 선택",
"fav_posts_deselect_all_button":"모두 선택 해제",
"fav_posts_download_selected_button":"선택 항목 다운로드",
"fav_posts_cancel_button":"취소",
"fav_posts_cookies_required_error":"오류: 즐겨찾는 게시물에는 쿠키가 필요하지만 로드할 수 없습니다.",
"fav_posts_auth_failed_title":"인증 실패 (게시물)",
"fav_posts_auth_failed_message":"인증 오류로 인해 {domain_specific_part}에서 즐겨찾기를 가져올 수 없습니다:\n\n{error_message}\n\n이는 일반적으로 사이트에 대한 쿠키가 없거나 유효하지 않거나 만료되었음을 의미합니다. 쿠키 설정을 확인하십시오.",
"fav_posts_fetch_error_title":"가져오기 오류",
"fav_posts_fetch_error_message":"{domain}{error_message_part}에서 즐겨찾기를 가져오는 중 오류 발생",
"fav_posts_no_posts_found_status":"즐겨찾는 게시물을 찾을 수 없습니다.",
"fav_posts_found_status":"{count}개의 즐겨찾는 게시물을 찾았습니다.",
"fav_posts_display_error_status":"게시물 표시 오류: {error}",
"fav_posts_ui_error_title":"UI 오류",
"fav_posts_ui_error_message":"즐겨찾는 게시물을 표시할 수 없습니다: {error}",
"fav_posts_auth_failed_message_generic":"인증 오류로 인해 {domain_specific_part}에서 즐겨찾기를 가져올 수 없습니다. 이는 일반적으로 사이트에 대한 쿠키가 없거나 유효하지 않거나 만료되었음을 의미합니다. 쿠키 설정을 확인하십시오.",
"key_fetching_fav_post_list_init":"즐겨찾는 게시물 목록 가져오는 중...",
"key_fetching_from_source_kemono_su":"Kemono.su에서 즐겨찾기 가져오는 중...",
"key_fetching_from_source_coomer_su":"Coomer.su에서 즐겨찾기 가져오는 중...",
"fav_posts_fetch_cancelled_status":"즐겨찾는 게시물 가져오기가 취소되었습니다.",
"known_names_filter_dialog_title":"필터에 알려진 이름 추가",
"known_names_filter_search_placeholder":"이름 검색...",
"known_names_filter_select_all_button":"모두 선택",
"known_names_filter_deselect_all_button":"모두 선택 해제",
"known_names_filter_add_selected_button":"선택 항목 추가",
"error_files_dialog_title":"오류로 인해 건너뛴 파일",
"error_files_no_errors_label":"마지막 세션 또는 재시도 후 오류로 인해 건너뛴 것으로 기록된 파일이 없습니다.",
"error_files_found_label":"다운로드 오류로 인해 다음 {count}개의 파일이 건너뛰어졌습니다:",
"error_files_select_all_button":"모두 선택",
"error_files_retry_selected_button":"선택 항목 다시 시도",
"error_files_export_urls_button":"URL을 .txt로 내보내기",
"error_files_no_selection_retry_message":"다시 시도할 파일을 하나 이상 선택하십시오.",
"error_files_no_errors_export_title":"오류 없음",
"error_files_no_errors_export_message":"내보낼 오류 파일 URL이 없습니다.",
"error_files_no_urls_found_export_title":"URL을 찾을 수 없음",
"error_files_no_urls_found_export_message":"내보낼 오류 파일 목록에서 URL을 추출할 수 없습니다.",
"error_files_save_dialog_title":"오류 파일 URL 저장",
"error_files_export_success_title":"내보내기 성공",
"error_files_export_success_message":"{count}개의 항목을 다음으로 성공적으로 내보냈습니다:\n{filepath}",
"error_files_export_error_title":"내보내기 오류",
"error_files_export_error_message":"파일 링크를 내보낼 수 없습니다: {error}",
"export_options_dialog_title":"내보내기 옵션",
"export_options_description_label":"오류 파일 링크를 내보낼 형식을 선택하십시오:",
"export_options_radio_link_only":"줄당 링크 (URL만)",
"export_options_radio_link_only_tooltip":"실패한 각 파일에 대한 직접 다운로드 URL만 내보냅니다. 줄당 하나의 URL.",
"export_options_radio_with_details":"세부 정보와 함께 내보내기 (URL [게시물, 파일 정보])",
"export_options_radio_with_details_tooltip":"URL 다음에 게시물 제목, 게시물 ID, 원본 파일 이름과 같은 세부 정보를 대괄호 안에 내보냅니다.",
"export_options_export_button":"내보내기",
"no_errors_logged_title":"기록된 오류 없음",
"no_errors_logged_message":"마지막 세션 또는 재시도 후 오류로 인해 건너뛴 것으로 기록된 파일이 없습니다.",
"progress_initializing_text":"진행률: 초기화 중...",
"progress_posts_text":"진행률: {processed_posts} / {total_posts} 게시물 ({progress_percent:.1f}%)",
"progress_processing_post_text":"진행률: 게시물 {processed_posts} 처리 중...",
"progress_starting_text":"진행률: 시작 중...",
"downloading_file_known_size_text":"'{filename}' 다운로드 중 ({downloaded_mb:.1f}MB / {total_mb:.1f}MB)",
"downloading_file_unknown_size_text":"'{filename}' 다운로드 중 ({downloaded_mb:.1f}MB)",
"downloading_multipart_text":"DL '{filename}...': {downloaded_mb:.1f}/{total_mb:.1f} MB ({parts} 파트 @ {speed:.2f} MB/s)",
"downloading_multipart_initializing_text":"파일: {filename} - 파트 초기화 중...",
"status_completed":"완료됨",
"status_cancelled_by_user":"사용자가 취소함",
"files_downloaded_label":"다운로드됨",
"files_skipped_label":"건너뜀",
"retry_finished_text":"재시도 완료",
"succeeded_text":"성공",
"failed_text":"실패",
"ready_for_new_task_text":"새 작업 준비 완료.",
"fav_mode_active_label_text":"⭐ 즐겨찾기 모드가 활성화되었습니다. 즐겨찾는 아티스트/게시물을 선택하기 전에 아래 필터를 선택하십시오. 아래 작업을 선택하십시오.",
"export_links_button_text":"링크 내보내기",
"download_extracted_links_button_text":"다운로드",
"download_selected_button_text":"선택 항목 다운로드",
"link_input_placeholder_text":"예: https://kemono.su/patreon/user/12345 또는 .../post/98765",
"link_input_tooltip_text":"Kemono/Coomer 작성자 페이지 또는 특정 게시물의 전체 URL을 입력하십시오.\n예 (작성자): https://kemono.su/patreon/user/12345\n예 (게시물): https://kemono.su/patreon/user/12345/post/98765",
"dir_input_placeholder_text":"다운로드 항목이 저장될 폴더를 선택하십시오",
"dir_input_tooltip_text":"모든 다운로드된 콘텐츠가 저장될 기본 폴더를 입력하거나 찾으십시오.\n'링크만' 모드를 선택하지 않은 경우 이 필드는 필수입니다.",
"character_input_placeholder_text":"예: Tifa, Aerith, (Cloud, Zack)",
"custom_folder_input_placeholder_text":"선택 사항: 이 게시물을 특정 폴더에 저장",
"custom_folder_input_tooltip_text":"단일 게시물 URL을 다운로드하고 '이름/제목별로 폴더 분리'가 활성화된 경우,\n해당 게시물의 다운로드 폴더에 대한 사용자 지정 이름을 여기에 입력할 수 있습니다.\n예: 내가 가장 좋아하는 장면",
"skip_words_input_placeholder_text":"예: WM, WIP, 스케치, 미리보기",
"remove_from_filename_input_placeholder_text":"예: patreon, HD",
"cookie_text_input_placeholder_no_file_selected_text":"쿠키 문자열 (cookies.txt가 선택되지 않은 경우)",
"cookie_text_input_placeholder_with_file_selected_text":"선택한 쿠키 파일 사용 중 (찾아보기... 참조)",
"character_search_input_placeholder_text":"캐릭터 검색...",
"character_search_input_tooltip_text":"아래 알려진 프로그램/캐릭터 목록을 필터링하려면 여기에 입력하십시오.",
"new_char_input_placeholder_text":"새 프로그램/캐릭터 이름 추가",
"new_char_input_tooltip_text":"위 목록에 추가할 새 프로그램, 게임 또는 캐릭터 이름을 입력하십시오.",
"link_search_input_placeholder_text":"링크 검색...",
"link_search_input_tooltip_text":"'링크만' 모드일 때 텍스트, URL 또는 플랫폼으로 표시된 링크를 필터링하려면 여기에 입력하십시오.",
"manga_date_prefix_input_placeholder_text":"만화 파일 이름 접두사",
"manga_date_prefix_input_tooltip_text":"'날짜 기반' 또는 '원본 파일' 만화 파일 이름에 대한 선택적 접두사(예: '시리즈 이름').\n비어 있으면 파일은 접두사 없이 스타일에 따라 이름이 지정됩니다.",
"log_display_mode_links_view_text":"🔗 링크 보기",
"log_display_mode_progress_view_text":"⬇️ 진행률 보기",
"download_external_links_dialog_title":"선택한 외부 링크 다운로드",
"select_all_button_text":"모두 선택",
"deselect_all_button_text":"모두 선택 해제",
"cookie_browse_button_tooltip":"쿠키 파일(Netscape 형식, 일반적으로 cookies.txt)을 찾으십시오.\n'쿠키 사용'이 선택되어 있고 위 텍스트 필드가 비어 있는 경우 사용됩니다.",
"page_range_label_text":"페이지 범위:",
"start_page_input_placeholder":"시작",
"start_page_input_tooltip":"작성자 URL의 경우: 다운로드할 시작 페이지 번호(예: 1, 2, 3)를 지정하십시오.\n첫 페이지부터 시작하려면 비워두거나 1로 설정하십시오.\n단일 게시물 URL 또는 만화/코믹 모드에서는 비활성화됩니다.",
"page_range_to_label_text":"에서",
"end_page_input_placeholder":"끝",
"end_page_input_tooltip":"작성자 URL의 경우: 다운로드할 끝 페이지 번호(예: 5, 10)를 지정하십시오.\n시작 페이지부터 모든 페이지를 다운로드하려면 비워두십시오.\n단일 게시물 URL 또는 만화/코믹 모드에서는 비활성화됩니다.",
"known_names_help_button_tooltip_text":"애플리케이션 기능 가이드 열기.",
"future_settings_button_tooltip_text":"애플리케이션 설정 열기 (테마, 언어 등).",
"link_search_button_tooltip_text":"표시된 링크 필터링",
"confirm_add_all_dialog_title":"새 이름 추가 확인",
"confirm_add_all_info_label":"'캐릭터로 필터링' 입력의 다음 새 이름/그룹이 'Known.txt'에 없습니다.\n이를 추가하면 향후 다운로드를 위한 폴더 구성을 개선할 수 있습니다.\n\n목록을 검토하고 작업을 선택하십시오:",
"confirm_add_all_select_all_button":"모두 선택",
"confirm_add_all_deselect_all_button":"모두 선택 해제",
"confirm_add_all_add_selected_button":"선택 항목을 Known.txt에 추가",
"confirm_add_all_skip_adding_button":"이 항목 추가 건너뛰기",
"confirm_add_all_cancel_download_button":"다운로드 취소",
"cookie_help_dialog_title":"쿠키 파일 지침",
"cookie_help_instruction_intro":"<p>쿠키를 사용하려면 일반적으로 브라우저에서 <b>cookies.txt</b> 파일이 필요합니다.</p>",
"cookie_help_how_to_get_title":"<p><b>cookies.txt를 얻는 방법:</b></p>",
"cookie_help_step1_extension_intro":"<li>Chrome 기반 브라우저용 'Get cookies.txt LOCALLY' 확장 프로그램을 설치하십시오:<br><a href=\"https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc\" style=\"color: #87CEEB;\">Chrome 웹 스토어에서 Get cookies.txt LOCALLY 받기</a></li>",
"cookie_help_step2_login":"<li>웹사이트(예: kemono.su 또는 coomer.su)로 이동하여 필요한 경우 로그인하십시오.</li>",
"cookie_help_step3_click_icon":"<li>브라우저 도구 모음에서 확장 프로그램 아이콘을 클릭하십시오.</li>",
"cookie_help_step4_export":"<li>'내보내기' 버튼(예: \"다른 이름으로 내보내기\", \"cookies.txt 내보내기\" - 정확한 문구는 확장 프로그램 버전에 따라 다를 수 있음)을 클릭하십시오.</li>",
"cookie_help_step5_save_file":"<li>다운로드한 <code>cookies.txt</code> 파일을 컴퓨터에 저장하십시오.</li>",
"cookie_help_step6_app_intro":"<li>이 애플리케이션에서:<ul>",
"cookie_help_step6a_checkbox":"<li>'쿠키 사용' 확인란이 선택되어 있는지 확인하십시오.</li>",
"cookie_help_step6b_browse":"<li>쿠키 텍스트 필드 옆에 있는 '찾아보기...' 버튼을 클릭하십시오.</li>",
"cookie_help_step6c_select":"<li>방금 저장한 <code>cookies.txt</code> 파일을 선택하십시오.</li></ul></li>",
"cookie_help_alternative_paste":"<p>또는 일부 확장 프로그램에서는 쿠키 문자열을 직접 복사할 수 있습니다. 그렇다면 파일을 찾는 대신 텍스트 필드에 붙여넣을 수 있습니다.</p>",
"cookie_help_proceed_without_button":"쿠키 없이 다운로드",
"empty_popup_button_tooltip_text": "크리에이터 선택 열기 (creators.json 찾아보기)",
"cookie_help_cancel_download_button":"다운로드 취소",
"character_input_tooltip":"캐릭터 이름을 쉼표로 구분하여 입력하십시오. 고급 그룹화를 지원하며 '폴더 분리'가 활성화된 경우 폴더 이름 지정에 영향을 줍니다.\n\n예:\n- Nami → 'Nami'와 일치, 'Nami' 폴더 생성.\n- (Ulti, Vivi) → 둘 중 하나와 일치, 'Ulti Vivi' 폴더, 둘 다 Known.txt에 별도로 추가.\n- (Boa, Hancock)~ → 둘 중 하나와 일치, 'Boa Hancock' 폴더, Known.txt에 하나의 그룹으로 추가.\n\n이름은 일치를 위한 별칭으로 처리됩니다.\n\n필터 모드 (버튼 순환):\n- 파일: 파일 이름으로 필터링.\n- 제목: 게시물 제목으로 필터링.\n- 둘 다: 제목 우선, 그 다음 파일 이름.\n- 댓글 (베타): 파일 이름 우선, 그 다음 게시물 댓글.",
"tour_dialog_title":"Kemono Downloader에 오신 것을 환영합니다!",
"tour_dialog_never_show_checkbox":"다시는 이 둘러보기를 표시하지 않음",
"tour_dialog_skip_button":"둘러보기 건너뛰기",
"tour_dialog_back_button":"뒤로",
"tour_dialog_next_button":"다음",
"tour_dialog_finish_button":"완료",
"tour_dialog_step1_title":"👋 환영합니다!",
"tour_dialog_step1_content":"안녕하세요! 이 빠른 둘러보기에서는 향상된 필터링, 만화 모드 개선 및 쿠키 관리와 같은 최근 업데이트를 포함하여 Kemono Downloader의 주요 기능을 안내합니다.\n<ul>\n<li>제 목표는 여러분이 <b>Kemono</b> 및 <b>Coomer</b>에서 콘텐츠를 쉽게 다운로드할 수 있도록 돕는 것입니다.</li><br>\n<li><b>🎨 작성자 선택 버튼:</b> URL 입력 옆에 있는 팔레트 아이콘을 클릭하여 대화 상자를 엽니다. <code>creators.json</code> 파일에서 작성자를 찾아보고 선택하여 URL 입력에 이름을 빠르게 추가하십시오.</li><br>\n<li><b>중요 팁: 앱이 '(응답 없음)' 상태인가요?</b><br>\n'다운로드 시작'을 클릭한 후, 특히 대규모 작성자 피드나 많은 스레드가 있는 경우 애플리케이션이 일시적으로 '(응답 없음)'으로 표시될 수 있습니다. 운영 체제(Windows, macOS, Linux)에서 '프로세스 종료' 또는 '강제 종료'를 제안할 수도 있습니다.<br>\n<b>기다려 주십시오!</b> 앱은 종종 백그라운드에서 열심히 작동하고 있습니다. 강제 종료하기 전에 파일 탐색기에서 선택한 '다운로드 위치'를 확인해 보십시오. 새 폴더가 생성되거나 파일이 나타나면 다운로드가 올바르게 진행되고 있음을 의미합니다. 다시 응답할 때까지 시간을 주십시오.</li><br>\n<li><b>다음</b> 및 <b>뒤로</b> 버튼을 사용하여 탐색하십시오.</li><br>\n<li>많은 옵션에는 자세한 내용을 보려면 마우스를 가져가면 나타나는 도구 설명이 있습니다.</li><br>\n<li>언제든지 이 가이드를 닫으려면 <b>둘러보기 건너뛰기</b>를 클릭하십시오.</li><br>\n<li>향후 시작 시 이 둘러보기를 보고 싶지 않으면 <b>'다시는 이 둘러보기를 표시하지 않음'</b>을 선택하십시오.</li>\n</ul>",
"tour_dialog_step2_title":"① 시작하기",
"tour_dialog_step2_content":"다운로드 기본 사항부터 시작하겠습니다:\n<ul>\n<li><b>🔗 Kemono 작성자/게시물 URL:</b><br>\n작성자 페이지의 전체 웹 주소(URL)(예: <i>https://kemono.su/patreon/user/12345</i>)\n또는 특정 게시물(예: <i>.../post/98765</i>)을 붙여넣으십시오.<br>\n또는 Coomer 작성자(예: <i>https://coomer.su/onlyfans/user/artistname</i>)</li><br>\n<li><b>📁 다운로드 위치:</b><br>\n'찾아보기...'를 클릭하여 다운로드한 모든 파일이 저장될 컴퓨터의 폴더를 선택하십시오.\n'링크만' 모드를 사용하지 않는 한 이 필드는 필수입니다.</li><br>\n<li><b>📄 페이지 범위 (작성자 URL만):</b><br>\n작성자 페이지에서 다운로드하는 경우 가져올 페이지 범위(예: 2-5페이지)를 지정할 수 있습니다.\n모든 페이지에 대해 비워두십시오. 단일 게시물 URL 또는 <b>만화/코믹 모드</b>가 활성화된 경우 이 기능은 비활성화됩니다.</li>\n</ul>",
"tour_dialog_step3_title":"② 다운로드 필터링",
"tour_dialog_step3_content":"이러한 필터로 다운로드할 항목을 구체화하십시오('링크만' 또는 '아카이브만' 모드에서는 대부분 비활성화됨):\n<ul>\n<li><b>🎯 캐릭터로 필터링:</b><br>\n캐릭터 이름을 쉼표로 구분하여 입력하십시오(예: <i>Tifa, Aerith</i>). 결합된 폴더 이름에 대한 별칭 그룹화: <i>(별칭1, 별칭2, 별칭3)</i>은 '별칭1 별칭2 별칭3' 폴더가 됩니다(정리 후). 그룹의 모든 이름은 일치를 위한 별칭으로 사용됩니다.<br>\n이 입력 옆에 있는 <b>'필터: [유형]'</b> 버튼은 이 필터가 적용되는 방식을 순환합니다:\n<ul><li><i>필터: 파일:</i> 개별 파일 이름을 확인합니다. 파일이 하나라도 일치하면 게시물이 유지됩니다. 일치하는 파일만 다운로드됩니다. 폴더 이름 지정은 일치하는 파일 이름의 캐릭터를 사용합니다('폴더 분리'가 켜져 있는 경우).</li><br>\n<li><i>필터: 제목:</i> 게시물 제목을 확인합니다. 일치하는 게시물의 모든 파일이 다운로드됩니다. 폴더 이름 지정은 일치하는 게시물 제목의 캐릭터를 사용합니다.</li>\n<li><b>⤵️ 필터에 추가 버튼 (알려진 이름):</b> 알려진 이름에 대한 '추가' 버튼 옆에 있습니다(5단계 참조). 팝업이 열립니다. <code>Known.txt</code> 목록에서 확인란(검색 창 포함)을 통해 이름을 선택하여 '캐릭터로 필터링' 필드에 빠르게 추가하십시오. <code>(Boa, Hancock)</code>와 같은 그룹화된 이름은 <code>(Boa, Hancock)~</code>로 필터에 추가됩니다.</li><br>\n<li><i>필터: 둘 다:</i> 먼저 게시물 제목을 확인합니다. 일치하면 모든 파일이 다운로드됩니다. 일치하지 않으면 파일 이름을 확인하고 일치하는 파일만 다운로드됩니다. 폴더 이름 지정은 제목 일치를 우선으로 하고 그 다음 파일 일치를 따릅니다.</li><br>\n<li><i>필터: 댓글 (베타):</i> 먼저 파일 이름을 확인합니다. 파일이 일치하면 게시물의 모든 파일이 다운로드됩니다. 파일이 일치하지 않으면 게시물 댓글을 확인합니다. 댓글이 일치하면 모든 파일이 다운로드됩니다. (더 많은 API 요청을 사용합니다). 폴더 이름 지정은 파일 일치를 우선으로 하고 그 다음 댓글 일치를 따릅니다.</li></ul>\n이 필터는 '이름/제목별로 폴더 분리'가 활성화된 경우 폴더 이름 지정에도 영향을 줍니다.</li><br>\n<li><b>🚫 단어로 건너뛰기:</b><br>\n쉼표로 구분된 단어(예: <i>WIP, 스케치, 미리보기</i>)를 입력하십시오.\n이 입력 옆에 있는 <b>'범위: [유형]'</b> 버튼은 이 필터가 적용되는 방식을 순환합니다:\n<ul><li><i>범위: 파일:</i> 파일 이름에 이 단어 중 하나라도 포함되어 있으면 파일을 건너뜁니다.</li><br>\n<li><i>범위: 게시물:</i> 게시물 제목에 이 단어 중 하나라도 포함되어 있으면 전체 게시물을 건너뜁니다.</li><br>\n<li><i>범위: 둘 다:</i> 파일 및 게시물 제목 건너뛰기를 모두 적용합니다(게시물 우선, 그 다음 파일).</li></ul></li><br>\n<li><b>파일 필터링 (라디오 버튼):</b> 다운로드할 항목을 선택하십시오:\n<ul>\n<li><i>전체:</i> 찾은 모든 파일 유형을 다운로드합니다.</li><br>\n<li><i>이미지/GIF:</i> 일반적인 이미지 형식 및 GIF만.</li><br>\n<li><i>비디오:</i> 일반적인 비디오 형식만.</li><br>\n<li><b><i>📦 아카이브만:</i></b> <b>.zip</b> 및 <b>.rar</b> 파일만 독점적으로 다운로드합니다. 이 옵션을 선택하면 '.zip 건너뛰기' 및 '.rar 건너뛰기' 확인란이 자동으로 비활성화되고 선택 취소됩니다. '외부 링크 표시'도 비활성화됩니다.</li><br>\n<li><i>🎧 오디오만:</i> 일반적인 오디오 형식(MP3, WAV, FLAC 등)만.</li><br>\n<li><i>🔗 링크만:</i> 파일을 다운로드하는 대신 게시물 설명에서 외부 링크를 추출하여 표시합니다. 다운로드 관련 옵션 및 '외부 링크 표시'는 비활성화됩니다.</li>\n</ul></li>\n</ul>",
"tour_dialog_step4_title":"③ 즐겨찾기 모드 (대체 다운로드)",
"tour_dialog_step4_content":"이 애플리케이션은 Kemono.su에서 즐겨찾기에 추가한 아티스트의 콘텐츠를 다운로드하기 위한 '즐겨찾기 모드'를 제공합니다.\n<ul>\n<li><b>⭐ 즐겨찾기 모드 확인란:</b><br>\n'🔗 링크만' 라디오 버튼 옆에 있습니다. 즐겨찾기 모드를 활성화하려면 이 확인란을 선택하십시오.</li><br>\n<li><b>즐겨찾기 모드에서 일어나는 일:</b>\n<ul><li>'🔗 Kemono 작성자/게시물 URL' 입력 영역이 즐겨찾기 모드가 활성화되었음을 나타내는 메시지로 바뀝니다.</li><br>\n<li>표준 '다운로드 시작', '일시 중지', '취소' 버튼이 '🖼️ 즐겨찾는 아티스트' 및 '📄 즐겨찾는 게시물' 버튼으로 바뀝니다(참고: '즐겨찾는 게시물'은 향후 예정).</li><br>\n<li>'🍪 쿠키 사용' 옵션은 즐겨찾기를 가져오는 데 쿠키가 필요하므로 자동으로 활성화되고 잠깁니다.</li></ul></li><br>\n<li><b>🖼️ 즐겨찾는 아티스트 버튼:</b><br>\nKemono.su에서 즐겨찾기에 추가한 아티스트 목록이 있는 대화 상자를 열려면 이 버튼을 클릭하십시오. 다운로드할 아티스트를 한 명 이상 선택할 수 있습니다.</li><br>\n<li><b>즐겨찾기 다운로드 범위 (버튼):</b><br>\n이 버튼('즐겨찾는 게시물' 옆)은 선택한 즐겨찾기가 다운로드되는 위치를 제어합니다:\n<ul><li><i>범위: 선택한 위치:</i> 선택한 모든 아티스트가 설정한 기본 '다운로드 위치'에 다운로드됩니다. 필터는 전역적으로 적용됩니다.</li><br>\n<li><i>범위: 아티스트 폴더:</i> 선택한 각 아티스트에 대해 기본 '다운로드 위치' 내에 하위 폴더(아티스트 이름)가 생성됩니다. 해당 아티스트의 콘텐츠는 특정 폴더로 이동합니다. 필터는 각 아티스트의 폴더 내에서 적용됩니다.</li></ul></li><br>\n<li><b>즐겨찾기 모드의 필터:</b><br>\n'캐릭터로 필터링', '단어로 건너뛰기' 및 '파일 필터링' 옵션은 선택한 즐겨찾는 아티스트에서 다운로드한 콘텐츠에 계속 적용됩니다.</li>\n</ul>",
"tour_dialog_step5_title":"④ 다운로드 미세 조정",
"tour_dialog_step5_content":"다운로드를 사용자 지정하는 추가 옵션:\n<ul>\n<li><b>.zip 건너뛰기 / .rar 건너뛰기:</b> 이러한 아카이브 파일 유형의 다운로드를 피하려면 이 확인란을 선택하십시오.\n<i>(참고: '📦 아카이브만' 필터 모드를 선택하면 비활성화되고 무시됩니다).</i></li><br>\n<li><b>✂️ 이름에서 단어 제거:</b><br>\n다운로드한 파일 이름에서 제거할 단어를 쉼표로 구분하여 입력하십시오(대소문자 구분 없음).</li><br>\n<li><b>썸네일만 다운로드:</b> 전체 크기 파일 대신 작은 미리보기 이미지를 다운로드합니다(사용 가능한 경우).</li><br>\n<li><b>대용량 이미지 압축:</b> 'Pillow' 라이브러리가 설치된 경우 WebP 버전이 훨씬 작으면 1.5MB보다 큰 이미지가 WebP 형식으로 변환됩니다.</li><br>\n<li><b>🗄️ 사용자 지정 폴더 이름 (단일 게시물만):</b><br>\n특정 단일 게시물 URL을 다운로드하고 '이름/제목별로 폴더 분리'가 활성화된 경우,\n해당 게시물의 다운로드 폴더에 대한 사용자 지정 이름을 여기에 입력할 수 있습니다.</li><br>\n<li><b>🍪 쿠키 사용:</b> 요청에 쿠키를 사용하려면 이 확인란을 선택하십시오. 다음 중 하나를 수행할 수 있습니다:\n<ul><li>쿠키 문자열을 텍스트 필드에 직접 입력하십시오(예: <i>name1=value1; name2=value2</i>).</li><br>\n<li>'찾아보기...'를 클릭하여 <i>cookies.txt</i> 파일(Netscape 형식)을 선택하십시오. 경로가 텍스트 필드에 나타납니다.</li></ul>\n이는 로그인이 필요한 콘텐츠에 액세스하는 데 유용합니다. 텍스트 필드는 채워진 경우 우선합니다.\n'쿠키 사용'이 선택되어 있지만 텍스트 필드와 찾아본 파일이 모두 비어 있으면 앱 디렉토리에서 'cookies.txt'를 로드하려고 시도합니다.</li>\n</ul>",
"tour_dialog_step6_title":"⑤ 구성 및 성능",
"tour_dialog_step6_content":"다운로드를 구성하고 성능을 관리하십시오:\n<ul>\n<li><b>⚙️ 이름/제목별로 폴더 분리:</b> '캐릭터로 필터링' 입력 또는 게시물 제목을 기반으로 하위 폴더를 만듭니다(<b>Known.txt</b> 목록을 폴더 이름의 대체 수단으로 사용할 수 있음).</li><br>\n<li><b>게시물당 하위 폴더:</b> '폴더 분리'가 켜져 있으면 기본 캐릭터/제목 폴더 내에 <i>각 개별 게시물</i>에 대한 추가 하위 폴더가 생성됩니다.</li><br>\n<li><b>🚀 멀티스레딩 사용 (스레드):</b> 더 빠른 작업을 활성화합니다. '스레드' 입력의 숫자는 다음을 의미합니다:\n<ul><li><b>작성자 피드:</b> 동시에 처리할 게시물 수. 각 게시물 내의 파일은 해당 작업자에 의해 순차적으로 다운로드됩니다('날짜 기반' 만화 이름 지정이 켜져 있지 않은 한, 이 경우 1개의 게시물 작업자가 강제됨).</li><br>\n<li><b>단일 게시물 URL:</b> 해당 단일 게시물에서 동시에 다운로드할 파일 수.</li></ul>\n선택하지 않으면 1개의 스레드가 사용됩니다. 스레드 수가 많으면(예: >40) 권장 사항이 표시될 수 있습니다.</li><br>\n<li><b>다중 파트 다운로드 전환 (로그 영역 오른쪽 상단):</b><br>\n<b>'다중 파트: [켜기/끄기]'</b> 버튼을 사용하여 개별 대용량 파일에 대한 다중 세그먼트 다운로드를 활성화/비활성화할 수 있습니다.\n<ul><li><b>켜기:</b> 대용량 파일(예: 비디오)의 다운로드 속도를 높일 수 있지만 작은 파일이 많은 경우 UI 끊김이나 로그 스팸이 증가할 수 있습니다. 활성화하면 권장 사항이 나타납니다. 다중 파트 다운로드가 실패하면 단일 스트림으로 다시 시도합니다.</li><br>\n<li><b>끄기 (기본값):</b> 파일은 단일 스트림으로 다운로드됩니다.</li></ul>\n'링크만' 또는 '아카이브만' 모드가 활성화된 경우 이 기능은 비활성화됩니다.</li><br>\n<li><b>📖 만화/코믹 모드 (작성자 URL만):</b> 순차적 콘텐츠에 맞게 조정되었습니다.\n<ul>\n<li>게시물을 <b>가장 오래된 것부터 최신 것까지</b> 다운로드합니다.</li><br>\n<li>모든 게시물이 가져오므로 '페이지 범위' 입력은 비활성화됩니다.</li><br>\n<li>작성자 피드에 이 모드가 활성화되면 로그 영역의 오른쪽 상단에 <b>파일 이름 스타일 전환 버튼</b>(예: '이름: 게시물 제목')이 나타납니다. 클릭하여 이름 지정 스타일을 순환하십시오:\n<ul>\n<li><b><i>이름: 게시물 제목 (기본값):</i></b> 게시물의 첫 번째 파일은 게시물의 정리된 제목(예: '내 1장.jpg')으로 이름이 지정됩니다. *동일한 게시물* 내의 후속 파일은 원래 파일 이름(예: 'page_02.png', 'bonus_art.jpg')을 유지하려고 시도합니다. 게시물에 파일이 하나만 있으면 게시물 제목으로 이름이 지정됩니다. 이는 대부분의 만화/코믹에 일반적으로 권장됩니다.</li><br>\n<li><b><i>이름: 원본 파일:</i></b> 모든 파일은 원래 파일 이름을 유지하려고 시도합니다. 스타일 버튼 옆에 나타나는 입력 필드에 선택적 접두사(예: '내 시리즈_')를 입력할 수 있습니다. 예: '내 시리즈_원본 파일.jpg'.</li><br>\n<li><b><i>이름: 제목+전역 번호 (게시물 제목 + 전역 번호 매기기):</i></b> 현재 다운로드 세션의 모든 게시물에 있는 모든 파일은 게시물의 정리된 제목을 접두사로 사용하고 전역 카운터를 사용하여 순차적으로 이름이 지정됩니다. 예: 게시물 '1장' (파일 2개) -> '1장_001.jpg', '1장_002.png'. 다음 게시물 '2장' (파일 1개)은 번호 매기기를 계속합니다 -> '2장_003.jpg'. 올바른 전역 번호 매기기를 보장하기 위해 이 스타일에 대한 게시물 처리 멀티스레딩은 자동으로 비활성화됩니다.</li><br>\n<li><b><i>이름: 날짜 기반:</i></b> 파일은 게시물 게시 순서에 따라 순차적으로 이름이 지정됩니다(001.ext, 002.ext, ...). 스타일 버튼 옆에 나타나는 입력 필드에 선택적 접두사(예: '내 시리즈_')를 입력할 수 있습니다. 예: '내 시리즈_001.jpg'. 이 스타일에 대한 게시물 처리 멀티스레딩은 자동으로 비활성화됩니다.</li>\n</ul>\n</li><br>\n<li>'이름: 게시물 제목', '이름: 제목+전역 번호' 또는 '이름: 날짜 기반' 스타일로 최상의 결과를 얻으려면 폴더 구성을 위해 '캐릭터로 필터링' 필드를 만화/시리즈 제목과 함께 사용하십시오.</li>\n</ul></li><br>\n<li><b>🎭 스마트 폴더 구성을 위한 Known.txt:</b><br>\n<code>Known.txt</code>(앱 디렉토리 내)는 '이름/제목별로 폴더 분리'가 활성화된 경우 자동 폴더 구성에 대한 세분화된 제어를 허용합니다.\n<ul>\n<li><b>작동 방식:</b> <code>Known.txt</code>의 각 줄은 항목입니다.\n<ul><li><code>내 멋진 시리즈</code>와 같은 간단한 줄은 이와 일치하는 콘텐츠가 '내 멋진 시리즈'라는 폴더로 이동함을 의미합니다.</li><br>\n<li><code>(캐릭터 A, 캐릭 A, 대체 이름 A)</code>와 같은 그룹화된 줄은 '캐릭터 A', '캐릭 A' 또는 '대체 이름 A'와 일치하는 콘텐츠가 모두 '캐릭터 A 캐릭 A 대체 이름 A'라는 단일 폴더(정리 후)로 이동함을 의미합니다. 괄호 안의 모든 용어는 해당 폴더의 별칭이 됩니다.</li></ul></li>\n<li><b>지능형 대체:</b> '이름/제목별로 폴더 분리'가 활성화되어 있고 게시물이 특정 '캐릭터로 필터링' 입력과 일치하지 않는 경우 다운로더는 <code>Known.txt</code>를 참조하여 폴더 생성을 위한 일치하는 기본 이름을 찾습니다.</li><br>\n<li><b>사용자 친화적인 관리:</b> 아래 UI 목록을 통해 간단한(그룹화되지 않은) 이름을 추가하십시오. 고급 편집(예: 그룹화된 별칭 생성/수정)의 경우 텍스트 편집기에서 파일을 편집하려면 <b>'Known.txt 열기'</b>를 클릭하십시오. 앱은 다음에 사용하거나 시작할 때 다시 로드합니다.</li>\n</ul>\n</li>\n</ul>",
"tour_dialog_step7_title":"⑥ 일반적인 오류 및 문제 해결",
"tour_dialog_step7_content":"때때로 다운로드에 문제가 발생할 수 있습니다. 다음은 몇 가지 일반적인 문제입니다:\n<ul>\n<li><b>캐릭터 입력 도구 설명:</b><br>\n캐릭터 이름을 쉼표로 구분하여 입력하십시오(예: <i>Tifa, Aerith</i>).<br>\n결합된 폴더 이름에 대한 별칭 그룹화: <i>(별칭1, 별칭2, 별칭3)</i>은 '별칭1 별칭2 별칭3' 폴더가 됩니다.<br>\n그룹의 모든 이름은 콘텐츠 일치를 위한 별칭으로 사용됩니다.<br><br>\n이 입력 옆에 있는 '필터: [유형]' 버튼은 이 필터가 적용되는 방식을 순환합니다:<br>\n- 필터: 파일: 개별 파일 이름을 확인합니다. 일치하는 파일만 다운로드됩니다.<br>\n- 필터: 제목: 게시물 제목을 확인합니다. 일치하는 게시물의 모든 파일이 다운로드됩니다.<br>\n- 필터: 둘 다: 먼저 게시물 제목을 확인합니다. 일치하지 않으면 파일 이름을 확인합니다.<br>\n- 필터: 댓글 (베타): 먼저 파일 이름을 확인합니다. 일치하지 않으면 게시물 댓글을 확인합니다.<br><br>\n이 필터는 '이름/제목별로 폴더 분리'가 활성화된 경우 폴더 이름 지정에도 영향을 줍니다.</li><br>\n<li><b>502 잘못된 게이트웨이 / 503 서비스를 사용할 수 없음 / 504 게이트웨이 시간 초과:</b><br>\n이는 일반적으로 Kemono/Coomer의 일시적인 서버 측 문제를 나타냅니다. 사이트가 과부하되었거나 유지 보수 중이거나 문제가 있을 수 있습니다.<br>\n<b>해결책:</b> 잠시 기다렸다가(예: 30분에서 몇 시간) 나중에 다시 시도하십시오. 브라우저에서 직접 사이트를 확인하십시오.</li><br>\n<li><b>연결 끊김 / 연결 거부 / 시간 초과 (파일 다운로드 중):</b><br>\n이는 인터넷 연결, 서버 불안정 또는 서버가 대용량 파일에 대한 연결을 끊는 경우 발생할 수 있습니다.<br>\n<b>해결책:</b> 인터넷을 확인하십시오. '스레드' 수가 많으면 줄여 보십시오. 앱은 세션이 끝날 때 일부 실패한 파일을 다시 시도하라는 메시지를 표시할 수 있습니다.</li><br>\n<li><b>IncompleteRead 오류:</b><br>\n서버가 예상보다 적은 데이터를 보냈습니다. 종종 일시적인 네트워크 문제 또는 서버 문제입니다.<br>\n<b>해결책:</b> 앱은 종종 다운로드 세션이 끝날 때 다시 시도하도록 이러한 파일을 표시합니다.</li><br>\n<li><b>403 금지됨 / 401 인증되지 않음 (공개 게시물에는 덜 일반적):</b><br>\n콘텐츠에 액세스할 권한이 없을 수 있습니다. 일부 유료 또는 비공개 콘텐츠의 경우 브라우저 세션의 유효한 쿠키와 함께 '쿠키 사용' 옵션을 사용하면 도움이 될 수 있습니다. 쿠키가 최신 상태인지 확인하십시오.</li><br>\n<li><b>404 찾을 수 없음:</b><br>\n게시물 또는 파일 URL이 잘못되었거나 콘텐츠가 사이트에서 제거되었습니다. URL을 다시 확인하십시오.</li><br>\n<li><b>'게시물을 찾을 수 없음' / '대상 게시물을 찾을 수 없음':</b><br>\nURL이 올바르고 작성자/게시물이 존재하는지 확인하십시오. 페이지 범위를 사용하는 경우 작성자에게 유효한지 확인하십시오. 매우 새로운 게시물의 경우 API에 나타나기까지 약간의 지연이 있을 수 있습니다.</li><br>\n<li><b>일반적인 느림 / 앱 '(응답 없음)':</b><br>\n1단계에서 언급했듯이 앱이 시작 후 중단된 것처럼 보이면, 특히 대규모 작성자 피드나 많은 스레드가 있는 경우 시간을 주십시오. 백그라운드에서 데이터를 처리하고 있을 가능성이 높습니다. 스레드 수를 줄이면 이러한 현상이 자주 발생하는 경우 응답성이 향상될 수 있습니다.</li>\n</ul>",
"tour_dialog_step8_title":"⑦ 로그 및 최종 제어",
"tour_dialog_step8_content":"모니터링 및 제어:\n<ul>\n<li><b>📜 진행률 로그 / 추출된 링크 로그:</b> 자세한 다운로드 메시지를 표시합니다. '🔗 링크만' 모드가 활성화된 경우 이 영역에 추출된 링크가 표시됩니다.</li><br>\n<li><b>로그에 외부 링크 표시:</b> 선택하면 주 로그 패널 아래에 보조 로그 패널이 나타나 게시물 설명에서 찾은 외부 링크를 표시합니다. <i>('🔗 링크만' 또는 '📦 아카이브만' 모드가 활성화된 경우 비활성화됨).</i></li><br>\n<li><b>로그 보기 전환 (👁️ / 🙈 버튼):</b><br>\n이 버튼(로그 영역 오른쪽 상단)은 주 로그 보기를 전환합니다:\n<ul><li><b>👁️ 진행률 로그 (기본값):</b> 모든 다운로드 활동, 오류 및 요약을 표시합니다.</li><br>\n<li><b>🙈 누락된 캐릭터 로그:</b> '캐릭터로 필터링' 설정으로 인해 건너뛴 게시물 제목의 주요 용어 목록을 표시합니다. 의도치 않게 놓치고 있는 콘텐츠를 식별하는 데 유용합니다.</li></ul></li><br>\n<li><b>🔄 재설정:</b> 모든 입력 필드, 로그를 지우고 임시 설정을 기본값으로 재설정합니다. 다운로드가 활성화되어 있지 않을 때만 사용할 수 있습니다.</li><br>\n<li><b>⬇️ 다운로드 시작 / 🔗 링크 추출 / ⏸️ 일시 중지 / ❌ 취소:</b> 이러한 버튼은 프로세스를 제어합니다. '취소 및 UI 재설정'은 현재 작업을 중지하고 URL 및 디렉토리 입력을 보존하면서 소프트 UI 재설정을 수행합니다. '일시 중지/재개'를 사용하면 일시적으로 중단하고 계속할 수 있습니다.</li><br>\n<li>일부 파일이 복구 가능한 오류('IncompleteRead' 등)로 실패하면 세션이 끝날 때 다시 시도하라는 메시지가 표시될 수 있습니다.</li>\n</ul>\n<br>모두 준비되었습니다! 둘러보기를 닫고 다운로더 사용을 시작하려면 <b>'완료'</b>를 클릭하십시오.",
"help_guide_dialog_title":"Kemono Downloader - 기능 가이드",
"help_guide_github_tooltip":"프로젝트의 GitHub 페이지 방문 (브라우저에서 열림)",
"help_guide_instagram_tooltip":"인스타그램 페이지 방문 (브라우저에서 열림)",
"help_guide_discord_tooltip":"Discord 커뮤니티 방문 (브라우저에서 열림)",
"help_guide_step1_title":"① 소개 및 주요 입력",
"help_guide_step1_content":"<html><head/><body>\n<p>이 가이드는 Kemono Downloader의 기능, 필드 및 버튼에 대한 개요를 제공합니다.</p>\n<h3>주요 입력 영역 (왼쪽 상단)</h3>\n<ul>\n<li><b>🔗 Kemono 작성자/게시물 URL:</b>\n<ul>\n<li>작성자 페이지의 전체 웹 주소(예: <i>https://kemono.su/patreon/user/12345</i>) 또는 특정 게시물(예: <i>.../post/98765</i>)을 입력하십시오.</li>\n<li>Kemono(kemono.su, kemono.party) 및 Coomer(coomer.su, coomer.party) URL을 지원합니다.</li>\n</ul>\n</li>\n<li><b>페이지 범위 (시작부터 끝까지):</b>\n<ul>\n<li>작성자 URL의 경우: 가져올 페이지 범위(예: 2-5페이지)를 지정하십시오. 모든 페이지에 대해 비워두십시오.</li>\n<li>단일 게시물 URL 또는 <b>만화/코믹 모드</b>가 활성화된 경우 비활성화됩니다.</li>\n</ul>\n</li>\n<li><b>📁 다운로드 위치:</b>\n<ul>\n<li><b>'찾아보기...'</b>를 클릭하여 다운로드한 모든 파일이 저장될 컴퓨터의 기본 폴더를 선택하십시오.</li>\n<li>'<b>🔗 링크만</b>' 모드를 사용하지 않는 한 이 필드는 필수입니다.</li>\n</ul>\n</li>\n<li><b>🎨 작성자 선택 버튼 (URL 입력 옆):</b>\n<ul>\n<li>팔레트 아이콘(🎨)을 클릭하여 '작성자 선택' 대화 상자를 엽니다.</li>\n<li>이 대화 상자는 <code>creators.json</code> 파일(애플리케이션 디렉토리에 있어야 함)에서 작성자를 로드합니다.</li>\n<li><b>대화 상자 내부:</b>\n<ul>\n<li><b>검색 창:</b> 이름이나 서비스로 작성자 목록을 필터링하려면 입력하십시오.</li>\n<li><b>작성자 목록:</b> <code>creators.json</code>의 작성자를 표시합니다. '즐겨찾기'에 추가한 작성자(JSON 데이터)가 맨 위에 표시됩니다.</li>\n<li><b>확인란:</b> 이름 옆에 있는 상자를 선택하여 한 명 이상의 작성자를 선택하십시오.</li>\n<li><b>'범위' 버튼 (예: '범위: 캐릭터'):</b> 이 버튼은 이 팝업에서 다운로드를 시작할 때 다운로드 구성을 전환합니다:\n<ul><li><i>범위: 캐릭터:</i> 다운로드는 기본 '다운로드 위치' 내에서 직접 캐릭터 이름의 폴더로 구성됩니다. 동일한 캐릭터에 대한 다른 작성자의 작품이 함께 그룹화됩니다.</li>\n<li><i>범위: 작성자:</i> 다운로드는 먼저 기본 '다운로드 위치' 내에 작성자 이름의 폴더를 만듭니다. 그런 다음 각 작성자의 폴더 내에 캐릭터 이름의 하위 폴더가 생성됩니다.</li></ul>\n</li>\n<li><b>'선택 항목 추가' 버튼:</b> 이 버튼을 클릭하면 선택한 모든 작성자의 이름을 가져와 쉼표로 구분하여 기본 '🔗 Kemono 작성자/게시물 URL' 입력 필드에 추가합니다. 그런 다음 대화 상자가 닫힙니다.</li>\n</ul>\n</li>\n<li>이 기능은 각 URL을 수동으로 입력하거나 붙여넣지 않고도 여러 작성자에 대한 URL 필드를 빠르게 채울 수 있는 방법을 제공합니다.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step2_title":"② 다운로드 필터링",
"help_guide_step2_content":"<html><head/><body>\n<h3>다운로드 필터링 (왼쪽 패널)</h3>\n<ul>\n<li><b>🎯 캐릭터로 필터링:</b>\n<ul>\n<li>이름을 쉼표로 구분하여 입력하십시오(예: <code>Tifa, Aerith</code>).</li>\n<li><b>공유 폴더에 대한 그룹화된 별칭 (별도의 Known.txt 항목):</b> <code>(Vivi, Ulti, Uta)</code>.\n<ul><li>'Vivi', 'Ulti' 또는 'Uta'와 일치하는 콘텐츠는 'Vivi Ulti Uta'라는 공유 폴더로 이동합니다(정리 후).</li>\n<li>이 이름이 새 이름이면 'Vivi', 'Ulti' 및 'Uta'를 <code>Known.txt</code>에 <i>별도의 개별 항목</i>으로 추가하라는 메시지가 표시됩니다.</li>\n</ul>\n</li>\n<li><b>공유 폴더에 대한 그룹화된 별칭 (단일 Known.txt 항목):</b> <code>(Yuffie, Sonon)~</code> (물결표 <code>~</code> 참고).\n<ul><li>'Yuffie' 또는 'Sonon'과 일치하는 콘텐츠는 'Yuffie Sonon'이라는 공유 폴더로 이동합니다.</li>\n<li>새로운 경우 'Yuffie Sonon'(별칭 Yuffie, Sonon 포함)을 <code>Known.txt</code>에 <i>단일 그룹 항목</i>으로 추가하라는 메시지가 표시됩니다.</li>\n</ul>\n</li>\n<li>이 필터는 '이름/제목별로 폴더 분리'가 활성화된 경우 폴더 이름 지정에 영향을 줍니다.</li>\n</ul>\n</li>\n<li><b>필터: [유형] 버튼 (캐릭터 필터 범위):</b> '캐릭터로 필터링'이 적용되는 방식을 순환합니다:\n<ul>\n<li><code>필터: 파일</code>: 개별 파일 이름을 확인합니다. 파일이 하나라도 일치하면 게시물이 유지됩니다. 일치하는 파일만 다운로드됩니다. 폴더 이름 지정은 일치하는 파일 이름의 캐릭터를 사용합니다.</li>\n<li><code>필터: 제목</code>: 게시물 제목을 확인합니다. 일치하는 게시물의 모든 파일이 다운로드됩니다. 폴더 이름 지정은 일치하는 게시물 제목의 캐릭터를 사용합니다.</li>\n<li><code>필터: 둘 다</code>: 먼저 게시물 제목을 확인합니다. 일치하면 모든 파일이 다운로드됩니다. 일치하지 않으면 파일 이름을 확인하고 일치하는 파일만 다운로드됩니다. 폴더 이름 지정은 제목 일치를 우선으로 하고 그 다음 파일 일치를 따릅니다.</li>\n<li><code>필터: 댓글 (베타)</code>: 먼저 파일 이름을 확인합니다. 파일이 일치하면 게시물의 모든 파일이 다운로드됩니다. 파일이 일치하지 않으면 게시물 댓글을 확인합니다. 댓글이 일치하면 모든 파일이 다운로드됩니다. (더 많은 API 요청을 사용합니다). 폴더 이름 지정은 파일 일치를 우선으로 하고 그 다음 댓글 일치를 따릅니다.</li>\n</ul>\n</li>\n<li><b>🗄️ 사용자 지정 폴더 이름 (단일 게시물만):</b>\n<ul>\n<li>단일 특정 게시물 URL을 다운로드하고 '이름/제목별로 폴더 분리'가 활성화된 경우에만 표시되고 사용할 수 있습니다.</li>\n<li>해당 단일 게시물의 다운로드 폴더에 대한 사용자 지정 이름을 지정할 수 있습니다.</li>\n</ul>\n</li>\n<li><b>🚫 단어로 건너뛰기:</b>\n<ul><li>특정 콘텐츠를 건너뛰려면 쉼표로 구분된 단어(예: <code>WIP, 스케치, 미리보기</code>)를 입력하십시오.</li></ul>\n</li>\n<li><b>범위: [유형] 버튼 (단어 건너뛰기 범위):</b> '단어로 건너뛰기'가 적용되는 방식을 순환합니다:\n<ul>\n<li><code>범위: 파일</code>: 파일 이름에 이 단어 중 하나라도 포함되어 있으면 개별 파일을 건너뜁니다.</li>\n<li><code>범위: 게시물</code>: 게시물 제목에 이 단어 중 하나라도 포함되어 있으면 전체 게시물을 건너뜁니다.</li>\n<li><code>범위: 둘 다</code>: 둘 다 적용합니다 (게시물 제목이 먼저, 그 다음 개별 파일).</li>\n</ul>\n</li>\n<li><b>✂️ 이름에서 단어 제거:</b>\n<ul><li>다운로드한 파일 이름에서 제거할 단어를 쉼표로 구분하여 입력하십시오(대소문자 구분 없음).</li></ul>\n</li>\n<li><b>파일 필터링 (라디오 버튼):</b> 다운로드할 항목을 선택하십시오:\n<ul>\n<li><code>전체</code>: 찾은 모든 파일 유형을 다운로드합니다.</li>\n<li><code>이미지/GIF</code>: 일반적인 이미지 형식(JPG, PNG, GIF, WEBP 등) 및 GIF만.</li>\n<li><code>비디오</code>: 일반적인 비디오 형식(MP4, MKV, WEBM, MOV 등)만.</li>\n<li><code>📦 아카이브만</code>: <b>.zip</b> 및 <b>.rar</b> 파일만 독점적으로 다운로드합니다. 이 옵션을 선택하면 '.zip 건너뛰기' 및 '.rar 건너뛰기' 확인란이 자동으로 비활성화되고 선택 취소됩니다. '외부 링크 표시'도 비활성화됩니다.</li>\n<li><code>🎧 오디오만</code>: 일반적인 오디오 형식(MP3, WAV, FLAC, M4A, OGG 등)만 다운로드합니다. 다른 파일 관련 옵션은 '이미지' 또는 '비디오' 모드와 동일하게 작동합니다.</li>\n<li><code>🔗 링크만</code>: 파일을 다운로드하는 대신 게시물 설명에서 외부 링크를 추출하여 표시합니다. 다운로드 관련 옵션 및 '외부 링크 표시'는 비활성화됩니다. 기본 다운로드 버튼이 '🔗 링크 추출'로 변경됩니다.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step3_title":"③ 다운로드 옵션 및 설정",
"help_guide_step3_content":"<html><head/><body>\n<h3>다운로드 옵션 및 설정 (왼쪽 패널)</h3>\n<ul>\n<li><b>.zip 건너뛰기 / .rar 건너뛰기:</b> 이러한 아카이브 파일 유형의 다운로드를 피하기 위한 확인란. ('📦 아카이브만' 필터 모드를 선택하면 비활성화되고 무시됨).</li>\n<li><b>썸네일만 다운로드:</b> 전체 크기 파일 대신 작은 미리보기 이미지를 다운로드합니다(사용 가능한 경우).</li>\n<li><b>대용량 이미지 압축 (WebP로):</b> 'Pillow'(PIL) 라이브러리가 설치된 경우 WebP 버전이 훨씬 작으면 1.5MB보다 큰 이미지가 WebP 형식으로 변환됩니다.</li>\n<li><b>⚙️ 고급 설정:</b>\n<ul>\n<li><b>이름/제목별로 폴더 분리:</b> '캐릭터로 필터링' 입력 또는 게시물 제목을 기반으로 하위 폴더를 만듭니다. <b>Known.txt</b> 목록을 폴더 이름의 대체 수단으로 사용할 수 있습니다.</li></ul></li></ul></body></html>",
"help_guide_step4_title":"④ 고급 설정 (1부)",
"help_guide_step4_content":"<html><head/><body><h3>⚙️ 고급 설정 (계속)</h3><ul><ul>\n<li><b>게시물당 하위 폴더:</b> '폴더 분리'가 켜져 있으면 기본 캐릭터/제목 폴더 내에 <i>각 개별 게시물</i>에 대한 추가 하위 폴더가 생성됩니다.</li>\n<li><b>쿠키 사용:</b> 요청에 쿠키를 사용하려면 이 확인란을 선택하십시오.\n<ul>\n<li><b>텍스트 필드:</b> 쿠키 문자열을 직접 입력하십시오(예: <code>name1=value1; name2=value2</code>).</li>\n<li><b>찾아보기...:</b> <code>cookies.txt</code> 파일(Netscape 형식)을 선택하십시오. 경로가 텍스트 필드에 나타납니다.</li>\n<li><b>우선 순위:</b> 텍스트 필드(채워진 경우)가 찾아본 파일보다 우선합니다. '쿠키 사용'이 선택되어 있지만 둘 다 비어 있으면 앱 디렉토리에서 <code>cookies.txt</code>를 로드하려고 시도합니다.</li>\n</ul>\n</li>\n<li><b>멀티스레딩 사용 및 스레드 입력:</b>\n<ul>\n<li>더 빠른 작업을 활성화합니다. '스레드' 입력의 숫자는 다음을 의미합니다:\n<ul>\n<li><b>작성자 피드:</b> 동시에 처리할 게시물 수. 각 게시물 내의 파일은 해당 작업자에 의해 순차적으로 다운로드됩니다('날짜 기반' 만화 이름 지정이 켜져 있지 않은 한, 이 경우 1개의 게시물 작업자가 강제됨).</li>\n<li><b>단일 게시물 URL:</b> 해당 단일 게시물에서 동시에 다운로드할 파일 수.</li>\n</ul>\n</li>\n<li>선택하지 않으면 1개의 스레드가 사용됩니다. 스레드 수가 많으면(예: >40) 권장 사항이 표시될 수 있습니다.</li>\n</ul>\n</li></ul></ul></body></html>",
"help_guide_step5_title":"⑤ 고급 설정 (2부) 및 작업",
"help_guide_step5_content":"<html><head/><body><h3>⚙️ 고급 설정 (계속)</h3><ul><ul>\n<li><b>로그에 외부 링크 표시:</b> 선택하면 주 로그 패널 아래에 보조 로그 패널이 나타나 게시물 설명에서 찾은 외부 링크를 표시합니다. ('🔗 링크만' 또는 '📦 아카이브만' 모드가 활성화된 경우 비활성화됨).</li>\n<li><b>📖 만화/코믹 모드 (작성자 URL만):</b> 순차적 콘텐츠에 맞게 조정되었습니다.\n<ul>\n<li>게시물을 <b>가장 오래된 것부터 최신 것까지</b> 다운로드합니다.</li>\n<li>모든 게시물이 가져오므로 '페이지 범위' 입력은 비활성화됩니다.</li>\n<li>작성자 피드에 이 모드가 활성화되면 로그 영역의 오른쪽 상단에 <b>파일 이름 스타일 전환 버튼</b>(예: '이름: 게시물 제목')이 나타납니다. 클릭하여 이름 지정 스타일을 순환하십시오:\n<ul>\n<li><code>이름: 게시물 제목 (기본값)</code>: 게시물의 첫 번째 파일은 게시물의 정리된 제목(예: '내 1장.jpg')으로 이름이 지정됩니다. *동일한 게시물* 내의 후속 파일은 원래 파일 이름(예: 'page_02.png', 'bonus_art.jpg')을 유지하려고 시도합니다. 게시물에 파일이 하나만 있으면 게시물 제목으로 이름이 지정됩니다. 이는 대부분의 만화/코믹에 일반적으로 권장됩니다.</li>\n<li><code>이름: 원본 파일</code>: 모든 파일은 원래 파일 이름을 유지하려고 시도합니다.</li>\n<li><code>이름: 원본 파일</code>: 모든 파일은 원래 파일 이름을 유지하려고 시도합니다. 이 스타일이 활성화되면 이 스타일 버튼 옆에 <b>선택적 파일 이름 접두사</b>(예: '내 시리즈_')에 대한 입력 필드가 나타납니다. 예: '내 시리즈_원본 파일.jpg'.</li>\n<li><code>이름: 제목+전역 번호 (게시물 제목 + 전역 번호 매기기)</code>: 현재 다운로드 세션의 모든 게시물에 있는 모든 파일은 게시물의 정리된 제목을 접두사로 사용하고 전역 카운터를 사용하여 순차적으로 이름이 지정됩니다. 예: 게시물 '1장' (파일 2개) -> '1장 001.jpg', '1장 002.png'. 다음 게시물 '2장' (파일 1개) -> '2장 003.jpg'. 올바른 전역 번호 매기기를 보장하기 위해 이 스타일에 대한 게시물 처리 멀티스레딩은 자동으로 비활성화됩니다.</li>\n<li><code>이름: 날짜 기반</code>: 파일은 게시물 게시 순서에 따라 순차적으로 이름이 지정됩니다(001.ext, 002.ext, ...). 이 스타일이 활성화되면 이 스타일 버튼 옆에 <b>선택적 파일 이름 접두사</b>(예: '내 시리즈_')에 대한 입력 필드가 나타납니다. 예: '내 시리즈_001.jpg'. 이 스타일에 대한 게시물 처리 멀티스레딩은 자동으로 비활성화됩니다.</li>\n</ul>\n</li>\n<li>'이름: 게시물 제목', '이름: 제목+전역 번호' 또는 '이름: 날짜 기반' 스타일로 최상의 결과를 얻으려면 폴더 구성을 위해 '캐릭터로 필터링' 필드를 만화/시리즈 제목과 함께 사용하십시오.</li>\n</ul>\n</li>\n</ul></li></ul>\n<h3>주요 작업 버튼 (왼쪽 패널)</h3>\n<ul>\n<li><b>⬇️ 다운로드 시작 / 🔗 링크 추출:</b> 이 버튼의 텍스트와 기능은 '파일 필터링' 라디오 버튼 선택에 따라 변경됩니다. 주요 작업을 시작합니다.</li>\n<li><b>⏸️ 다운로드 일시 중지 / ▶️ 다운로드 재개:</b> 현재 다운로드/추출 프로세스를 일시적으로 중단하고 나중에 재개할 수 있습니다. 일시 중지된 동안 일부 UI 설정을 변경할 수 있습니다.</li>\n<li><b>❌ 취소 및 UI 재설정:</b> 현재 작업을 중지하고 소프트 UI 재설정을 수행합니다. URL 및 다운로드 디렉토리 입력은 보존되지만 다른 설정 및 로그는 지워집니다.</li>\n</ul></body></html>",
"help_guide_step6_title":"⑥ 알려진 프로그램/캐릭터 목록",
"help_guide_step6_content":"<html><head/><body>\n<h3>알려진 프로그램/캐릭터 목록 관리 (왼쪽 하단)</h3>\n<p>이 섹션은 '이름/제목별로 폴더 분리'가 활성화된 경우 스마트 폴더 구성을 위해 사용되는 <code>Known.txt</code> 파일을 관리하는 데 도움이 됩니다. 특히 게시물이 활성 '캐릭터로 필터링' 입력과 일치하지 않는 경우 대체 수단으로 사용됩니다.</p>\n<ul>\n<li><b>Known.txt 열기:</b> 기본 텍스트 편집기에서 <code>Known.txt</code> 파일(앱 디렉토리에 있음)을 열어 고급 편집(예: 복잡한 그룹화된 별칭 생성)을 수행합니다.</li>\n<li><b>캐릭터 검색...:</b> 아래에 표시된 알려진 이름 목록을 필터링합니다.</li>\n<li><b>목록 위젯:</b> <code>Known.txt</code>의 기본 이름을 표시합니다. 여기에서 항목을 선택하여 삭제하십시오.</li>\n<li><b>새 프로그램/캐릭터 이름 추가 (입력 필드):</b> 추가할 이름이나 그룹을 입력하십시오.\n<ul>\n<li><b>간단한 이름:</b> 예: <code>내 멋진 시리즈</code>. 단일 항목으로 추가됩니다.</li>\n<li><b>별도의 Known.txt 항목에 대한 그룹:</b> 예: <code>(Vivi, Ulti, Uta)</code>. 'Vivi', 'Ulti' 및 'Uta'를 <code>Known.txt</code>에 세 개의 별도 개별 항목으로 추가합니다.</li>\n<li><b>공유 폴더 및 단일 Known.txt 항목에 대한 그룹 (물결표 <code>~</code>):</b> 예: <code>(캐릭터 A, 캐릭 A)~</code>. <code>Known.txt</code>에 '캐릭터 A 캐릭 A'라는 하나의 항목을 추가합니다. '캐릭터 A'와 '캐릭 A'는 이 단일 폴더/항목의 별칭이 됩니다.</li>\n</ul>\n</li>\n<li><b>➕ 추가 버튼:</b> 위 입력 필드의 이름/그룹을 목록과 <code>Known.txt</code>에 추가합니다.</li>\n<li><b>⤵️ 필터에 추가 버튼:</b>\n<ul>\n<li>'알려진 프로그램/캐릭터' 목록의 '➕ 추가' 버튼 옆에 있습니다.</li>\n<li>이 버튼을 클릭하면 <code>Known.txt</code> 파일의 모든 이름이 각각 확인란과 함께 표시되는 팝업 창이 열립니다.</li>\n<li>팝업에는 이름 목록을 빠르게 필터링하기 위한 검색 창이 포함되어 있습니다.</li>\n<li>확인란을 사용하여 하나 이상의 이름을 선택할 수 있습니다.</li>\n<li>'선택 항목 추가'를 클릭하여 선택한 이름을 기본 창의 '캐릭터로 필터링' 입력 필드에 삽입하십시오.</li>\n<li><code>Known.txt</code>에서 선택한 이름이 원래 그룹인 경우(예: Known.txt에서 <code>(Boa, Hancock)</code>으로 정의됨), <code>(Boa, Hancock)~</code>로 필터 필드에 추가됩니다. 간단한 이름은 그대로 추가됩니다.</li>\n<li>편의를 위해 팝업에서 '모두 선택' 및 '모두 선택 해제' 버튼을 사용할 수 있습니다.</li>\n<li>변경 없이 팝업을 닫으려면 '취소'를 클릭하십시오.</li>\n</ul>\n</li>\n<li><b>🗑️ 선택 항목 삭제 버튼:</b> 목록과 <code>Known.txt</code>에서 선택한 이름을 삭제합니다.</li>\n<li><b>❓ 버튼 (바로 이것!):</b> 이 포괄적인 도움말 가이드를 표시합니다.</li>\n</ul></body></html>",
"help_guide_step7_title":"⑦ 로그 영역 및 제어",
"help_guide_step7_content":"<html><head/><body>\n<h3>로그 영역 및 제어 (오른쪽 패널)</h3>\n<ul>\n<li><b>📜 진행률 로그 / 추출된 링크 로그 (레이블):</b> 기본 로그 영역의 제목, '🔗 링크만' 모드가 활성화된 경우 변경됩니다.</li>\n<li><b>링크 검색... / 🔍 버튼 (링크 검색):</b>\n<ul><li>'🔗 링크만' 모드가 활성화된 경우에만 표시됩니다. 기본 로그에 표시된 추출된 링크를 텍스트, URL 또는 플랫폼으로 실시간 필터링할 수 있습니다.</li></ul>\n</li>\n<li><b>이름: [스타일] 버튼 (만화 파일 이름 스타일):</b>\n<ul><li>작성자 피드에 대해 <b>만화/코믹 모드</b>가 활성화되어 있고 '링크만' 또는 '아카이브만' 모드가 아닌 경우에만 표시됩니다.</li>\n<li>파일 이름 스타일을 순환합니다: <code>게시물 제목</code>, <code>원본 파일</code>, <code>날짜 기반</code>. (자세한 내용은 만화/코믹 모드 섹션 참조).</li>\n<li>'원본 파일' 또는 '날짜 기반' 스타일이 활성화되면 이 버튼 옆에 <b>선택적 파일 이름 접두사</b>에 대한 입력 필드가 나타납니다.</li>\n</ul>\n</li>\n<li><b>다중 파트: [켜기/끄기] 버튼:</b>\n<ul><li>개별 대용량 파일에 대한 다중 세그먼트 다운로드를 전환합니다.\n<ul><li><b>켜기:</b> 대용량 파일(예: 비디오)의 다운로드 속도를 높일 수 있지만 작은 파일이 많은 경우 UI 끊김이나 로그 스팸이 증가할 수 있습니다. 활성화하면 권장 사항이 나타납니다. 다중 파트 다운로드가 실패하면 단일 스트림으로 다시 시도합니다.</li>\n<li><b>끄기 (기본값):</b> 파일은 단일 스트림으로 다운로드됩니다.</li>\n</ul>\n<li>'🔗 링크만' 또는 '📦 아카이브만' 모드가 활성화된 경우 비활성화됩니다.</li>\n</ul>\n</li>\n<li><b>👁️ / 🙈 버튼 (로그 보기 전환):</b> 기본 로그 보기를 전환합니다:\n<ul>\n<li><b>👁️ 진행률 로그 (기본값):</b> 모든 다운로드 활동, 오류 및 요약을 표시합니다.</li>\n<li><b>🙈 누락된 캐릭터 로그:</b> '캐릭터로 필터링' 설정으로 인해 건너뛴 게시물 제목/콘텐츠의 주요 용어 목록을 표시합니다. 의도치 않게 놓치고 있는 콘텐츠를 식별하는 데 유용합니다.</li>\n</ul>\n</li>\n<li><b>🔄 재설정 버튼:</b> 모든 입력 필드, 로그를 지우고 임시 설정을 기본값으로 재설정합니다. 다운로드가 활성화되어 있지 않을 때만 사용할 수 있습니다.</li>\n<li><b>기본 로그 출력 (텍스트 영역):</b> 자세한 진행률 메시지, 오류 및 요약을 표시합니다. '🔗 링크만' 모드가 활성화된 경우 이 영역에 추출된 링크가 표시됩니다.</li>\n<li><b>누락된 캐릭터 로그 출력 (텍스트 영역):</b> (👁️ / 🙈 토글을 통해 볼 수 있음) 캐릭터 필터로 인해 건너뛴 게시물/파일을 표시합니다.</li>\n<li><b>외부 로그 출력 (텍스트 영역):</b> '로그에 외부 링크 표시'가 선택된 경우 기본 로그 아래에 나타납니다. 게시물 설명에서 찾은 외부 링크를 표시합니다.</li>\n<li><b>링크 내보내기 버튼:</b>\n<ul><li>'🔗 링크만' 모드가 활성화되어 있고 링크가 추출된 경우에만 표시되고 활성화됩니다.</li>\n<li>추출된 모든 링크를 <code>.txt</code> 파일에 저장할 수 있습니다.</li>\n</ul>\n</li>\n<li><b>진행률: [상태] 레이블:</b> 다운로드 또는 링크 추출 프로세스의 전체 진행률(예: 처리된 게시물)을 표시합니다.</li>\n<li><b>파일 진행률 레이블:</b> 속도 및 크기 또는 다중 파트 다운로드 상태를 포함하여 개별 파일 다운로드의 진행률을 표시합니다.</li>\n</ul></body></html>",
"help_guide_step8_title":"⑧ 즐겨찾기 모드 및 향후 기능",
"help_guide_step8_content":"<html><head/><body>\n<h3>즐겨찾기 모드 (Kemono.su 즐겨찾기에서 다운로드)</h3>\n<p>이 모드를 사용하면 Kemono.su에서 즐겨찾기에 추가한 아티스트의 콘텐츠를 직접 다운로드할 수 있습니다.</p>\n<ul>\n<li><b>⭐ 활성화 방법:</b>\n<ul>\n<li>'🔗 링크만' 라디오 버튼 옆에 있는 <b>'⭐ 즐겨찾기 모드'</b> 확인란을 선택하십시오.</li>\n</ul>\n</li>\n<li><b>즐겨찾기 모드의 UI 변경 사항:</b>\n<ul>\n<li>'🔗 Kemono 작성자/게시물 URL' 입력 영역이 즐겨찾기 모드가 활성화되었음을 나타내는 메시지로 바뀝니다.</li>\n<li>표준 '다운로드 시작', '일시 중지', '취소' 버튼이 다음으로 바뀝니다:\n<ul>\n<li><b>'🖼️ 즐겨찾는 아티스트'</b> 버튼</li>\n<li><b>'📄 즐겨찾는 게시물'</b> 버튼</li>\n</ul>\n</li>\n<li>'🍪 쿠키 사용' 옵션은 즐겨찾기를 가져오는 데 쿠키가 필요하므로 자동으로 활성화되고 잠깁니다.</li>\n</ul>\n</li>\n<li><b>🖼️ 즐겨찾는 아티스트 버튼:</b>\n<ul>\n<li>이 버튼을 클릭하면 Kemono.su에서 즐겨찾기에 추가한 모든 아티스트 목록이 있는 대화 상자가 열립니다.</li>\n<li>이 목록에서 한 명 이상의 아티스트를 선택하여 콘텐츠를 다운로드할 수 있습니다.</li>\n</ul>\n</li>\n<li><b>📄 즐겨찾는 게시물 버튼 (향후 기능):</b>\n<ul>\n<li>특정 즐겨찾기 <i>게시물</i>(특히 시리즈의 일부인 경우 만화와 같은 순차적 순서)을 다운로드하는 것은 현재 개발 중인 기능입니다.</li>\n<li>즐겨찾는 게시물, 특히 만화와 같은 순차적 읽기를 처리하는 가장 좋은 방법은 아직 탐색 중입니다.</li>\n<li>즐겨찾는 게시물을 다운로드하고 구성하는 방법에 대한 구체적인 아이디어나 사용 사례가 있는 경우(예: 즐겨찾기에서 '만화 스타일'), 프로젝트의 GitHub 페이지에서 문제를 제기하거나 토론에 참여하는 것을 고려해 보십시오. 여러분의 의견은 소중합니다!</li>\n</ul>\n</li>\n<li><b>즐겨찾기 다운로드 범위 (버튼):</b>\n<ul>\n<li>이 버튼('즐겨찾는 게시물' 옆)은 선택한 즐겨찾는 아티스트의 콘텐츠가 다운로드되는 위치를 제어합니다:\n<ul>\n<li><b><i>범위: 선택한 위치:</i></b> 선택한 모든 아티스트가 UI에서 설정한 기본 '다운로드 위치'에 다운로드됩니다. 필터는 모든 콘텐츠에 전역적으로 적용됩니다.</li>\n<li><b><i>범위: 아티스트 폴더:</i></b> 선택한 각 아티스트에 대해 기본 '다운로드 위치' 내에 하위 폴더(아티스트 이름)가 자동으로 생성됩니다. 해당 아티스트의 콘텐츠는 특정 하위 폴더로 이동합니다. 필터는 각 아티스트의 전용 폴더 내에서 적용됩니다.</li>\n</ul>\n</li>\n</ul>\n</li>\n<li><b>즐겨찾기 모드의 필터:</b>\n<ul>\n<li>UI에서 설정한 '🎯 캐릭터로 필터링', '🚫 단어로 건너뛰기' 및 '파일 필터링' 옵션은 선택한 즐겨찾는 아티스트에서 다운로드한 콘텐츠에 계속 적용됩니다.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step9_title":"⑨ 주요 파일 및 둘러보기",
"help_guide_step9_content":"<html><head/><body>\n<h3>애플리케이션에서 사용하는 주요 파일</h3>\n<ul>\n<li><b><code>Known.txt</code>:</b>\n<ul>\n<li>애플리케이션 디렉토리(<code>.exe</code> 또는 <code>main.py</code>가 있는 위치)에 있습니다.</li>\n<li>'이름/제목별로 폴더 분리'가 활성화된 경우 자동 폴더 구성을 위해 알려진 프로그램, 캐릭터 또는 시리즈 제목 목록을 저장합니다.</li>\n<li><b>형식:</b>\n<ul>\n<li>각 줄은 항목입니다.</li>\n<li><b>간단한 이름:</b> 예: <code>내 멋진 시리즈</code>. 이와 일치하는 콘텐츠는 '내 멋진 시리즈'라는 폴더로 이동합니다.</li>\n<li><b>그룹화된 별칭:</b> 예: <code>(캐릭터 A, 캐릭 A, 대체 이름 A)</code>. '캐릭터 A', '캐릭 A' 또는 '대체 이름 A'와 일치하는 콘텐츠는 모두 '캐릭터 A 캐릭 A 대체 이름 A'라는 단일 폴더(정리 후)로 이동합니다. 괄호 안의 모든 용어는 해당 폴더의 별칭이 됩니다.</li>\n</ul>\n</li>\n<li><b>사용법:</b> 게시물이 활성 '캐릭터로 필터링' 입력과 일치하지 않는 경우 폴더 이름 지정의 대체 수단으로 사용됩니다. UI를 통해 간단한 항목을 관리하거나 복잡한 별칭에 대해 파일을 직접 편집할 수 있습니다. 앱은 시작하거나 다음에 사용할 때 다시 로드합니다.</li>\n</ul>\n</li>\n<li><b><code>cookies.txt</code> (선택 사항):</b>\n<ul>\n<li>'쿠키 사용' 기능을 사용하고 직접 쿠키 문자열을 제공하거나 특정 파일을 찾지 않으면 애플리케이션은 해당 디렉토리에서 <code>cookies.txt</code>라는 파일을 찾습니다.</li>\n<li><b>형식:</b> Netscape 쿠키 파일 형식이어야 합니다.</li>\n<li><b>사용법:</b> 다운로더가 브라우저의 로그인 세션을 사용하여 Kemono/Coomer에서 로그인해야 할 수 있는 콘텐츠에 액세스할 수 있도록 합니다.</li>\n</ul>\n</li>\n</ul>\n<h3>처음 사용자 둘러보기</h3>\n<ul>\n<li>처음 실행 시(또는 재설정된 경우) 주요 기능을 안내하는 환영 둘러보기 대화 상자가 나타납니다. 건너뛰거나 '다시는 이 둘러보기를 표시하지 않음'을 선택할 수 있습니다.</li>\n</ul>\n<p><em>많은 UI 요소에는 마우스를 가져가면 나타나는 도구 설명도 있어 빠른 힌트를 제공합니다.</em></p>\n</body></html>"
})

translations ["es"]={}
translations ["es"].update ({
"settings_dialog_title":"Configuración",
"language_label":"Idioma:",
"lang_english":"Inglés (English)",
"lang_japanese":"Japonés (日本語)",
"theme_toggle_light":"Cambiar a modo claro",
"theme_toggle_dark":"Cambiar a modo oscuro",
"theme_tooltip_light":"Cambiar la apariencia de la aplicación a claro.",
"theme_tooltip_dark":"Cambiar la apariencia de la aplicación a oscuro.",
"ok_button":"Aceptar",
"appearance_group_title":"Apariencia",
"language_group_title":"Configuración de idioma",
"creator_post_url_label":"🔗 URL del creador/publicación de Kemono:",
"download_location_label":"📁 Ubicación de descarga:",
"filter_by_character_label":"🎯 Filtrar por personaje(s) (separados por comas):",
"skip_with_words_label":"🚫 Omitir con palabras (separadas por comas):",
"remove_words_from_name_label":"✂️ Eliminar palabras del nombre:",
"filter_all_radio":"Todo",
"filter_images_radio":"Imágenes/GIF",
"filter_videos_radio":"Vídeos",
"filter_archives_radio":"📦 Solo archivos comprimidos",
"filter_links_radio":"🔗 Solo enlaces",
"filter_audio_radio":"🎧 Solo audio",
"favorite_mode_checkbox_label":"⭐ Modo Favoritos",
"browse_button_text":"Explorar...",
"char_filter_scope_files_text":"Filtro: Archivos",
"char_filter_scope_files_tooltip":"Ámbito actual: Archivos\n\nFiltra archivos individuales por nombre. Una publicación se conserva si algún archivo coincide.\nSolo se descargan los archivos coincidentes de esa publicación.\nEjemplo: Filtro 'Tifa'. El archivo 'Tifa_artwork.jpg' coincide y se descarga.\nNomenclatura de carpetas: Usa el personaje del nombre del archivo coincidente.\n\nHaga clic para cambiar a: Ambos",
"char_filter_scope_title_text":"Filtro: Título",
"char_filter_scope_title_tooltip":"Ámbito actual: Título\n\nFiltra publicaciones completas por su título. Se descargan todos los archivos de una publicación coincidente.\nEjemplo: Filtro 'Aerith'. La publicación titulada 'El jardín de Aerith' coincide; se descargan todos sus archivos.\nNomenclatura de carpetas: Usa el personaje del título de la publicación coincidente.\n\nHaga clic para cambiar a: Archivos",
"char_filter_scope_both_text":"Filtro: Ambos",
"char_filter_scope_both_tooltip":"Ámbito actual: Ambos (Título y luego Archivos)\n\n1. Comprueba el título de la publicación: Si coincide, se descargan todos los archivos de la publicación.\n2. Si el título no coincide, comprueba los nombres de los archivos: Si algún archivo coincide, solo se descarga ese archivo.\nEjemplo: Filtro 'Cloud'.\n - Publicación 'Cloud Strife' (coincidencia de título) -> se descargan todos los archivos.\n - Publicación 'Persecución en moto' con 'Cloud_fenrir.jpg' (coincidencia de archivo) -> solo se descarga 'Cloud_fenrir.jpg'.\nNomenclatura de carpetas: Prioriza la coincidencia del título, luego la coincidencia del archivo.\n\nHaga clic para cambiar a: Comentarios",
"char_filter_scope_comments_text":"Filtro: Comentarios (Beta)",
"char_filter_scope_comments_tooltip":"Ámbito actual: Comentarios (Beta - Archivos primero, luego Comentarios como respaldo)\n\n1. Comprueba los nombres de los archivos: Si algún archivo de la publicación coincide con el filtro, se descarga la publicación completa. NO se comprueban los comentarios para este término de filtro.\n2. Si ningún archivo coincide, ENTONCES comprueba los comentarios de la publicación: Si un comentario coincide, se descarga la publicación completa.\nEjemplo: Filtro 'Barret'.\n - Publicación A: Archivos 'Barret_gunarm.jpg', 'other.png'. El archivo 'Barret_gunarm.jpg' coincide. Se descargan todos los archivos de la Publicación A. No se comprueban los comentarios para 'Barret'.\n - Publicación B: Archivos 'dyne.jpg', 'weapon.gif'. Comentarios: '...un dibujo de Barret Wallace...'. No hay coincidencia de archivo para 'Barret'. El comentario coincide. Se descargan todos los archivos de la Publicación B.\nNomenclatura de carpetas: Prioriza el personaje de la coincidencia del archivo, luego de la coincidencia del comentario.\n\nHaga clic para cambiar a: Título",
"char_filter_scope_unknown_text":"Filtro: Desconocido",
"char_filter_scope_unknown_tooltip":"Ámbito actual: Desconocido\n\nEl ámbito del filtro de personajes se encuentra en un estado desconocido. Por favor, cambie o reinicie.\n\nHaga clic para cambiar a: Título",
"skip_words_input_tooltip":"Introduzca palabras, separadas por comas, para omitir la descarga de cierto contenido (p. ej., WIP, sketch, preview).\n\nEl botón 'Ámbito: [Tipo]' junto a esta entrada alterna cómo se aplica este filtro:\n- Ámbito: Archivos: Omite archivos individuales si sus nombres contienen alguna de estas palabras.\n- Ámbito: Publicaciones: Omite publicaciones completas si sus títulos contienen alguna de estas palabras.\n- Ámbito: Ambos: Aplica ambos (primero el título de la publicación, luego los archivos individuales si el título de la publicación es correcto).",
"remove_words_input_tooltip":"Introduzca palabras, separadas por comas, para eliminarlas de los nombres de los archivos descargados (no distingue mayúsculas y minúsculas).\nÚtil para limpiar prefijos/sufijos comunes.\nEjemplo: patreon, kemono, [HD], _final",
"skip_scope_files_text":"Ámbito: Archivos",
"skip_scope_files_tooltip":"Ámbito de omisión actual: Archivos\n\nOmite archivos individuales si sus nombres contienen alguna de las 'Palabras a omitir'.\nEjemplo: Omitir palabras \"WIP, sketch\".\n- Archivo \"art_WIP.jpg\" -> OMITIDO.\n- Archivo \"final_art.png\" -> DESCARGADO (si se cumplen otras condiciones).\n\nLa publicación sigue siendo procesada para otros archivos no omitidos.\nHaga clic para cambiar a: Ambos",
"skip_scope_posts_text":"Ámbito: Publicaciones",
"skip_scope_posts_tooltip":"Ámbito de omisión actual: Publicaciones\n\nOmite publicaciones completas si sus títulos contienen alguna de las 'Palabras a omitir'.\nSe ignoran todos los archivos de una publicación omitida.\nEjemplo: Omitir palabras \"preview, announcement\".\n- Publicación \"¡Anuncio emocionante!\" -> OMITIDA.\n- Publicación \"Obra de arte terminada\" -> PROCESADA (si se cumplen otras condiciones).\n\nHaga clic para cambiar a: Archivos",
"skip_scope_both_text":"Ámbito: Ambos",
"skip_scope_both_tooltip":"Ámbito de omisión actual: Ambos (Publicaciones y luego Archivos)\n\n1. Comprueba el título de la publicación: Si el título contiene una palabra a omitir, se OMITE la publicación completa.\n2. Si el título de la publicación es correcto, comprueba los nombres de los archivos individuales: Si un nombre de archivo contiene una palabra a omitir, solo se OMITE ese archivo.\nEjemplo: Omitir palabras \"WIP, sketch\".\n- Publicación \"Bocetos y WIPs\" (coincidencia de título) -> PUBLICACIÓN COMPLETA OMITIDA.\n- Publicación \"Actualización de arte\" (título correcto) con los archivos:\n  - \"character_WIP.jpg\" (coincidencia de archivo) -> OMITIDO.\n  - \"final_scene.png\" (archivo correcto) -> DESCARGADO.\n\nHaga clic para cambiar a: Publicaciones",
"skip_scope_unknown_text":"Ámbito: Desconocido",
"skip_scope_unknown_tooltip":"El ámbito de las palabras a omitir se encuentra en un estado desconocido. Por favor, cambie o reinicie.\n\nHaga clic para cambiar a: Publicaciones",
"language_change_title":"Idioma cambiado",
"language_change_message":"El idioma ha sido cambiado. Es necesario reiniciar para que todos los cambios surtan efecto.",
"language_change_informative":"¿Desea reiniciar la aplicación ahora?",
"restart_now_button":"Reiniciar ahora",
"skip_zip_checkbox_label":"Omitir .zip",
"skip_rar_checkbox_label":"Omitir .rar",
"download_thumbnails_checkbox_label":"Descargar solo miniaturas",
"scan_content_images_checkbox_label":"Escanear contenido en busca de imágenes",
"compress_images_checkbox_label":"Comprimir a WebP",
"separate_folders_checkbox_label":"Carpetas separadas por Nombre/Título",
"subfolder_per_post_checkbox_label":"Subcarpeta por publicación",
"use_cookie_checkbox_label":"Usar cookie",
"use_multithreading_checkbox_base_label":"Usar multihilo",
"show_external_links_checkbox_label":"Mostrar enlaces externos en el registro",
"manga_comic_mode_checkbox_label":"Modo Manga/Cómic",
"threads_label":"Hilos:",
"start_download_button_text":"⬇️ Iniciar descarga",
"start_download_button_tooltip":"Haga clic para iniciar el proceso de descarga o extracción de enlaces con la configuración actual.",
"extract_links_button_text":"🔗 Extraer enlaces",
"pause_download_button_text":"⏸️ Pausar descarga",
"pause_download_button_tooltip":"Haga clic para pausar el proceso de descarga en curso.",
"resume_download_button_text":"▶️ Reanudar descarga",
"resume_download_button_tooltip":"Haga clic para reanudar la descarga.",
"cancel_button_text":"❌ Cancelar y reiniciar UI",
"cancel_button_tooltip":"Haga clic para cancelar el proceso de descarga/extracción en curso y reiniciar los campos de la UI (conservando la URL y el Directorio).",
"error_button_text":"Error",
"error_button_tooltip":"Ver archivos omitidos debido a errores y, opcionalmente, reintentarlos.",
"cancel_retry_button_text":"❌ Cancelar reintento",
"known_chars_label_text":"🎭 Espectáculos/Personajes conocidos (para nombres de carpetas):",
"open_known_txt_button_text":"Abrir Known.txt",
"known_chars_list_tooltip":"Esta lista contiene nombres utilizados para la creación automática de carpetas cuando 'Carpetas separadas' está activado\ny no se proporciona ningún 'Filtrar por personaje(s)' específico o no coincide con una publicación.\nAñada nombres de series, juegos o personajes que descargue con frecuencia.",
"open_known_txt_button_tooltip":"Abrir el archivo 'Known.txt' en su editor de texto predeterminado.\nEl archivo se encuentra en el directorio de la aplicación.",
"add_char_button_text":"➕ Añadir",
"add_char_button_tooltip":"Añadir el nombre del campo de entrada a la lista 'Espectáculos/Personajes conocidos'.",
"add_to_filter_button_text":"⤵️ Añadir al filtro",
"add_to_filter_button_tooltip":"Seleccione nombres de la lista 'Espectáculos/Personajes conocidos' para añadirlos al campo 'Filtrar por personaje(s)' de arriba.",
"delete_char_button_text":"🗑️ Eliminar seleccionados",
"delete_char_button_tooltip":"Eliminar los nombres seleccionados de la lista 'Espectáculos/Personajes conocidos'.",
"progress_log_label_text":"📜 Registro de progreso:",
"radio_all_tooltip":"Descargar todos los tipos de archivos encontrados en las publicaciones.",
"radio_images_tooltip":"Descargar solo formatos de imagen comunes (JPG, PNG, GIF, WEBP, etc.).",
"radio_videos_tooltip":"Descargar solo formatos de vídeo comunes (MP4, MKV, WEBM, MOV, etc.).",
"radio_only_archives_tooltip":"Descargar exclusivamente archivos .zip y .rar. Otras opciones específicas de archivos están desactivadas.",
"radio_only_audio_tooltip":"Descargar solo formatos de audio comunes (MP3, WAV, FLAC, etc.).",
"radio_only_links_tooltip":"Extraer y mostrar enlaces externos de las descripciones de las publicaciones en lugar de descargar archivos.\nLas opciones relacionadas con la descarga se desactivarán.",
"favorite_mode_checkbox_tooltip":"Habilite el Modo Favoritos para explorar artistas/publicaciones guardados.\nEsto reemplazará la entrada de URL con botones de selección de Favoritos.",
"skip_zip_checkbox_tooltip":"Si se marca, no se descargarán los archivos de archivado .zip.\n(Desactivado si se selecciona 'Solo archivos comprimidos').",
"skip_rar_checkbox_tooltip":"Si se marca, no se descargarán los archivos de archivado .rar.\n(Desactivado si se selecciona 'Solo archivos comprimidos').",
"download_thumbnails_checkbox_tooltip":"Descarga pequeñas imágenes de vista previa de la API en lugar de archivos de tamaño completo (si están disponibles).\nSi también se marca 'Escanear contenido de la publicación en busca de URL de imágenes', este modo *solo* descargará las imágenes encontradas por el escaneo de contenido (ignorando las miniaturas de la API).",
"scan_content_images_checkbox_tooltip":"Si se marca, el descargador escaneará el contenido HTML de las publicaciones en busca de URL de imágenes (de etiquetas <img> o enlaces directos).\nEsto incluye la resolución de rutas relativas de las etiquetas <img> a URL completas.\nLas rutas relativas en las etiquetas <img> (p. ej., /data/image.jpg) se resolverán a URL completas.\nÚtil para casos en los que las imágenes están en la descripción de la publicación pero no en la lista de archivos/adjuntos de la API.",
"compress_images_checkbox_tooltip":"Comprimir imágenes > 1.5MB a formato WebP (requiere Pillow).",
"use_subfolders_checkbox_tooltip":"Crear subcarpetas basadas en la entrada 'Filtrar por personaje(s)' o en los títulos de las publicaciones.\nUtiliza la lista 'Espectáculos/Personajes conocidos' como respaldo para los nombres de las carpetas si ningún filtro específico coincide.\nActiva la entrada 'Filtrar por personaje(s)' y 'Nombre de carpeta personalizado' para publicaciones individuales.",
"use_subfolder_per_post_checkbox_tooltip":"Crea una subcarpeta para cada publicación. Si 'Carpetas separadas' también está activado, está dentro de la carpeta del personaje/título.",
"use_cookie_checkbox_tooltip":"Si se marca, intentará usar las cookies de 'cookies.txt' (formato Netscape)\nen el directorio de la aplicación para las solicitudes.\nÚtil para acceder a contenido que requiere inicio de sesión en Kemono/Coomer.",
"cookie_text_input_tooltip":"Introduzca su cadena de cookies directamente.\nSe usará si 'Usar cookie' está marcado Y 'cookies.txt' no se encuentra o este campo no está vacío.\nEl formato depende de cómo lo analizará el backend (p. ej., 'nombre1=valor1; nombre2=valor2').",
"use_multithreading_checkbox_tooltip":"Activa operaciones concurrentes. Consulte la entrada 'Hilos' para más detalles.",
"thread_count_input_tooltip":"Número de operaciones concurrentes.\n- Publicación única: Descargas de archivos concurrentes (se recomiendan 1-10).\n- URL del feed del creador: Número de publicaciones a procesar simultáneamente (se recomiendan 1-200).\n  Los archivos dentro de cada publicación son descargados uno por uno por su trabajador.\nSi 'Usar multihilo' no está marcado, se usa 1 hilo.",
"external_links_checkbox_tooltip":"Si se marca, aparecerá un panel de registro secundario debajo del registro principal para mostrar los enlaces externos encontrados en las descripciones de las publicaciones.\n(Desactivado si está activo el modo 'Solo enlaces' o 'Solo archivos comprimidos').",
"manga_mode_checkbox_tooltip":"Descarga las publicaciones de la más antigua a la más nueva y renombra los archivos según el título de la publicación (solo para feeds de creadores).",
"multipart_on_button_text":"Multihilo: ON",
"multipart_on_button_tooltip":"Descarga multihilo: ON\n\nHabilita la descarga de archivos grandes en múltiples segmentos simultáneamente.\n- Puede acelerar las descargas de archivos grandes individuales (p. ej., vídeos).\n- Puede aumentar el uso de la CPU/red.\n- Para feeds con muchos archivos pequeños, esto podría no ofrecer ventajas de velocidad y podría hacer que la UI/registro se vuelva denso.\n- Si la descarga multihilo falla, se reintenta como una transmisión única.\n\nHaga clic para desactivar.",
"multipart_off_button_text":"Multihilo: OFF",
"multipart_off_button_tooltip":"Descarga multihilo: OFF\n\nTodos los archivos se descargan usando una sola transmisión.\n- Estable y funciona bien para la mayoría de los escenarios, especialmente para muchos archivos más pequeños.\n- Los archivos grandes se descargan secuencialmente.\n\nHaga clic para activar (ver advertencia).",
"reset_button_text":"🔄 Reiniciar",
"reset_button_tooltip":"Reiniciar todas las entradas y registros al estado predeterminado (solo cuando está inactivo).",
"progress_idle_text":"Progreso: Inactivo",
"missed_character_log_label_text":"🚫 Registro de personajes omitidos:",
"creator_popup_title":"Selección de creador",
"creator_popup_search_placeholder":"Buscar por nombre, servicio o pegar URL del creador...",
"creator_popup_add_selected_button":"Añadir seleccionados",
"creator_popup_scope_characters_button":"Ámbito: Personajes",
"creator_popup_scope_creators_button":"Ámbito: Creadores",
"favorite_artists_button_text":"🖼️ Artistas favoritos",
"favorite_artists_button_tooltip":"Explore y descargue de sus artistas favoritos en Kemono.su/Coomer.su.",
"favorite_posts_button_text":"📄 Publicaciones favoritas",
"favorite_posts_button_tooltip":"Explore y descargue sus publicaciones favoritas de Kemono.su/Coomer.su.",
"favorite_scope_selected_location_text":"Ámbito: Ubicación seleccionada",
"favorite_scope_selected_location_tooltip":"Ámbito de descarga de favoritos actual: Ubicación seleccionada\n\nTodos los artistas/publicaciones favoritos seleccionados se descargarán en la 'Ubicación de descarga' principal especificada en la UI.\nLos filtros (personaje, palabras a omitir, tipo de archivo) se aplicarán globalmente a todo el contenido.\n\nHaga clic para cambiar a: Carpetas de artistas",
"favorite_scope_artist_folders_text":"Ámbito: Carpetas de artistas",
"favorite_scope_artist_folders_tooltip":"Ámbito de descarga de favoritos actual: Carpetas de artistas\n\nPara cada artista/publicación favorito seleccionado, se creará una nueva subcarpeta (con el nombre del artista) dentro de la 'Ubicación de descarga' principal.\nEl contenido de ese artista/publicación se descargará en su subcarpeta específica.\nLos filtros (personaje, palabras a omitir, tipo de archivo) se aplicarán *dentro* de la carpeta de cada artista.\n\nHaga clic para cambiar a: Ubicación seleccionada",
"favorite_scope_unknown_text":"Ámbito: Desconocido",
"favorite_scope_unknown_tooltip":"El ámbito de descarga de favoritos es desconocido. Haga clic para cambiar.",
"manga_style_post_title_text":"Nombre: Título de la publicación",
"manga_style_original_file_text":"Nombre: Archivo original",
"manga_style_date_based_text":"Nombre: Basado en la fecha",
"manga_style_title_global_num_text":"Nombre: Título+Núm.G.",
"manga_style_unknown_text":"Nombre: Estilo desconocido",
"fav_artists_dialog_title":"Artistas favoritos",
"fav_artists_loading_status":"Cargando artistas favoritos...",
"fav_artists_search_placeholder":"Buscar artistas...",
"fav_artists_select_all_button":"Seleccionar todo",
"fav_artists_deselect_all_button":"Deseleccionar todo",
"fav_artists_download_selected_button":"Descargar seleccionados",
"fav_artists_cancel_button":"Cancelar",
"fav_artists_loading_from_source_status":"⏳ Cargando favoritos de {source_name}...",
"fav_artists_found_status":"Se encontraron {count} artistas favoritos en total.",
"fav_artists_none_found_status":"No se encontraron artistas favoritos en Kemono.su o Coomer.su.",
"fav_artists_failed_status":"Error al obtener los favoritos.",
"fav_artists_cookies_required_status":"Error: Las cookies están habilitadas pero no se pudieron cargar para ninguna fuente.",
"fav_artists_no_favorites_after_processing":"No se encontraron artistas favoritos después del procesamiento.",
"fav_artists_no_selection_title":"Sin selección",
"fav_artists_no_selection_message":"Por favor, seleccione al menos un artista para descargar.",
"fav_posts_dialog_title":"Publicaciones favoritas",
"fav_posts_loading_status":"Cargando publicaciones favoritas...",
"fav_posts_search_placeholder":"Buscar publicaciones (título, creador, ID, servicio)...",
"fav_posts_select_all_button":"Seleccionar todo",
"fav_posts_deselect_all_button":"Deseleccionar todo",
"fav_posts_download_selected_button":"Descargar seleccionados",
"fav_posts_cancel_button":"Cancelar",
"fav_posts_cookies_required_error":"Error: Se requieren cookies para las publicaciones favoritas pero no se pudieron cargar.",
"fav_posts_auth_failed_title":"Error de autorización (Publicaciones)",
"fav_posts_auth_failed_message":"No se pudieron obtener los favoritos{domain_specific_part} debido a un error de autorización:\n\n{error_message}\n\nEsto generalmente significa que sus cookies faltan, no son válidas o han caducado para el sitio. Por favor, compruebe la configuración de sus cookies.",
"fav_posts_fetch_error_title":"Error de obtención",
"fav_posts_fetch_error_message":"Error al obtener los favoritos de {domain}{error_message_part}",
"fav_posts_no_posts_found_status":"No se encontraron publicaciones favoritas.",
"fav_posts_found_status":"Se encontraron {count} publicaciones favoritas.",
"fav_posts_display_error_status":"Error al mostrar las publicaciones: {error}",
"fav_posts_ui_error_title":"Error de UI",
"fav_posts_ui_error_message":"No se pudieron mostrar las publicaciones favoritas: {error}",
"fav_posts_auth_failed_message_generic":"No se pudieron obtener los favoritos{domain_specific_part} debido a un error de autorización. Esto generalmente significa que sus cookies faltan, no son válidas o han caducado para el sitio. Por favor, compruebe la configuración de sus cookies.",
"key_fetching_fav_post_list_init":"Obteniendo la lista de publicaciones favoritas...",
"key_fetching_from_source_kemono_su":"Obteniendo los favoritos de Kemono.su...",
"key_fetching_from_source_coomer_su":"Obteniendo los favoritos de Coomer.su...",
"fav_posts_fetch_cancelled_status":"Obtención de publicaciones favoritas cancelada.",
"known_names_filter_dialog_title":"Añadir nombres conocidos al filtro",
"known_names_filter_search_placeholder":"Buscar nombres...",
"known_names_filter_select_all_button":"Seleccionar todo",
"known_names_filter_deselect_all_button":"Deseleccionar todo",
"known_names_filter_add_selected_button":"Añadir seleccionados",
"error_files_dialog_title":"Archivos omitidos debido a errores",
"error_files_no_errors_label":"No se registraron archivos omitidos debido a errores en la última sesión o después de los reintentos.",
"error_files_found_label":"Los siguientes {count} archivos fueron omitidos debido a errores de descarga:",
"error_files_select_all_button":"Seleccionar todo",
"error_files_retry_selected_button":"Reintentar seleccionados",
"error_files_export_urls_button":"Exportar URL a .txt",
"error_files_no_selection_retry_message":"Por favor, seleccione al menos un archivo para reintentar.",
"error_files_no_errors_export_title":"Sin errores",
"error_files_no_errors_export_message":"No hay URL de archivos de error para exportar.",
"error_files_no_urls_found_export_title":"No se encontraron URL",
"error_files_no_urls_found_export_message":"No se pudo extraer ninguna URL de la lista de archivos de error para exportar.",
"error_files_save_dialog_title":"Guardar URL de archivos de error",
"error_files_export_success_title":"Exportación exitosa",
"error_files_export_success_message":"Se exportaron correctamente {count} entradas a:\n{filepath}",
"error_files_export_error_title":"Error de exportación",
"error_files_export_error_message":"No se pudieron exportar los enlaces de los archivos: {error}",
"export_options_dialog_title":"Opciones de exportación",
"export_options_description_label":"Elija el formato para exportar los enlaces de los archivos de error:",
"export_options_radio_link_only":"Enlace por línea (solo URL)",
"export_options_radio_link_only_tooltip":"Exporta solo la URL de descarga directa de cada archivo fallido, una URL por línea.",
"export_options_radio_with_details":"Exportar con detalles (URL [Publicación, Información del archivo])",
"export_options_radio_with_details_tooltip":"Exporta la URL seguida de detalles como el Título de la publicación, el ID de la publicación y el Nombre de archivo original entre corchetes.",
"export_options_export_button":"Exportar",
"no_errors_logged_title":"No se registraron errores",
"no_errors_logged_message":"No se registraron archivos omitidos debido a errores en la última sesión o después de los reintentos.",
"progress_initializing_text":"Progreso: Inicializando...",
"progress_posts_text":"Progreso: {processed_posts} / {total_posts} publicaciones ({progress_percent:.1f}%)",
"progress_processing_post_text":"Progreso: Procesando publicación {processed_posts}...",
"progress_starting_text":"Progreso: Iniciando...",
"downloading_file_known_size_text":"Descargando '{filename}' ({downloaded_mb:.1f}MB / {total_mb:.1f}MB)",
"downloading_file_unknown_size_text":"Descargando '{filename}' ({downloaded_mb:.1f}MB)",
"downloading_multipart_text":"DL '{filename}...': {downloaded_mb:.1f}/{total_mb:.1f} MB ({parts} partes @ {speed:.2f} MB/s)",
"downloading_multipart_initializing_text":"Archivo: {filename} - Inicializando partes...",
"status_completed":"Completado",
"status_cancelled_by_user":"Cancelado por el usuario",
"files_downloaded_label":"descargados",
"files_skipped_label":"omitidos",
"retry_finished_text":"Reintento finalizado",
"succeeded_text":"Exitoso",
"failed_text":"Fallido",
"ready_for_new_task_text":"Listo para una nueva tarea.",
"fav_mode_active_label_text":"⭐Elija los filtros a continuación antes de seleccionar sus favoritos.",
"export_links_button_text":"Exportar enlaces",
"download_extracted_links_button_text":"Descargar",
"download_selected_button_text":"Descargar seleccionados",
"link_input_placeholder_text":"p. ej., https://kemono.su/patreon/user/12345 o .../post/98765",
"link_input_tooltip_text":"Introduzca la URL completa de la página de un creador de Kemono/Coomer o de una publicación específica.\nEjemplo (Creador): https://kemono.su/patreon/user/12345\nEjemplo (Publicación): https://kemono.su/patreon/user/12345/post/98765",
"dir_input_placeholder_text":"Seleccione la carpeta donde se guardarán las descargas",
"dir_input_tooltip_text":"Introduzca o explore la carpeta principal donde se guardará todo el contenido descargado.\nEste campo es obligatorio a menos que se seleccione el modo 'Solo enlaces'.",
"character_input_placeholder_text":"p. ej., Tifa, Aerith, (Cloud, Zack)",
"custom_folder_input_placeholder_text":"Opcional: Guardar esta publicación en una carpeta específica",
"custom_folder_input_tooltip_text":"Si está descargando una URL de publicación única Y 'Carpetas separadas por Nombre/Título' está habilitado,\npuede introducir un nombre personalizado aquí para la carpeta de descarga de esa publicación.\nEjemplo: Mi escena favorita",
"skip_words_input_placeholder_text":"p. ej., WM, WIP, sketch, preview",
"remove_from_filename_input_placeholder_text":"p. ej., patreon, HD",
"cookie_text_input_placeholder_no_file_selected_text":"Cadena de cookies (si no se selecciona cookies.txt)",
"cookie_text_input_placeholder_with_file_selected_text":"Usando el archivo de cookies seleccionado (ver Explorar...)",
"character_search_input_placeholder_text":"Buscar personajes...",
"character_search_input_tooltip_text":"Escriba aquí para filtrar la lista de espectáculos/personajes conocidos a continuación.",
"new_char_input_placeholder_text":"Añadir nuevo nombre de espectáculo/personaje",
"new_char_input_tooltip_text":"Introduzca un nuevo nombre de espectáculo, juego o personaje para añadirlo a la lista de arriba.",
"link_search_input_placeholder_text":"Buscar enlaces...",
"link_search_input_tooltip_text":"En el modo 'Solo enlaces', escriba aquí para filtrar los enlaces mostrados por texto, URL o plataforma.",
"manga_date_prefix_input_placeholder_text":"Prefijo para nombres de archivo de manga",
"manga_date_prefix_input_tooltip_text":"Prefijo opcional para nombres de archivo de manga 'Basado en la fecha' u 'Archivo original' (p. ej., 'Nombre de la serie').\nSi está vacío, los archivos se nombrarán según el estilo sin prefijo.",
"log_display_mode_links_view_text":"🔗 Vista de enlaces",
"log_display_mode_progress_view_text":"⬇️ Vista de progreso",
"download_external_links_dialog_title":"Descargar enlaces externos seleccionados",
"select_all_button_text":"Seleccionar todo",
"deselect_all_button_text":"Deseleccionar todo",
"cookie_browse_button_tooltip":"Explore un archivo de cookies (formato Netscape, normalmente cookies.txt).\nSe usará si 'Usar cookie' está marcado y el campo de texto de arriba está vacío.",
"page_range_label_text":"Rango de páginas:",
"start_page_input_placeholder":"Inicio",
"start_page_input_tooltip":"Para URL de creadores: Especifique el número de página de inicio desde el que descargar (p. ej., 1, 2, 3).\nDéjelo en blanco o establézcalo en 1 para empezar desde la primera página.\nDesactivado para URL de publicaciones únicas o en Modo Manga/Cómic.",
"page_range_to_label_text":"a",
"end_page_input_placeholder":"Fin",
"end_page_input_tooltip":"Para URL de creadores: Especifique el número de página final hasta el que descargar (p. ej., 5, 10).\nDéjelo en blanco para descargar todas las páginas desde la página de inicio.\nDesactivado para URL de publicaciones únicas o en Modo Manga/Cómic.",
"known_names_help_button_tooltip_text":"Abrir la guía de funciones de la aplicación.",
"future_settings_button_tooltip_text":"Abrir la configuración de la aplicación (Tema, Idioma, etc.).",
"link_search_button_tooltip_text":"Filtrar los enlaces mostrados",
"confirm_add_all_dialog_title":"Confirmar la adición de nuevos nombres",
"confirm_add_all_info_label":"Los siguientes nombres/grupos nuevos de su entrada 'Filtrar por personaje(s)' no están en 'Known.txt'.\nAñadirlos puede mejorar la organización de las carpetas para futuras descargas.\n\nRevise la lista y elija una acción:",
"confirm_add_all_select_all_button":"Seleccionar todo",
"confirm_add_all_deselect_all_button":"Deseleccionar todo",
"confirm_add_all_add_selected_button":"Añadir seleccionados a Known.txt",
"confirm_add_all_skip_adding_button":"Omitir la adición de estos",
"confirm_add_all_cancel_download_button":"Cancelar descarga",
"cookie_help_dialog_title":"Instrucciones del archivo de cookies",
"cookie_help_instruction_intro":"<p>Para usar cookies, normalmente necesita un archivo <b>cookies.txt</b> de su navegador.</p>",
"cookie_help_how_to_get_title":"<p><b>Cómo obtener cookies.txt:</b></p>",
"cookie_help_step1_extension_intro":"<li>Instale la extensión 'Get cookies.txt LOCALLY' para su navegador basado en Chrome:<br><a href=\"https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc\" style=\"color: #87CEEB;\">Obtener cookies.txt LOCALLY en Chrome Web Store</a></li>",
"cookie_help_step2_login":"<li>Vaya al sitio web (p. ej., kemono.su o coomer.su) e inicie sesión si es necesario.</li>",
"cookie_help_step3_click_icon":"<li>Haga clic en el icono de la extensión en la barra de herramientas de su navegador.</li>",
"cookie_help_step4_export":"<li>Haga clic en un botón 'Exportar' (p. ej., \"Exportar como\", \"Exportar cookies.txt\" - la redacción exacta puede variar según la versión de la extensión).</li>",
"cookie_help_step5_save_file":"<li>Guarde el archivo <code>cookies.txt</code> descargado en su ordenador.</li>",
"cookie_help_step6_app_intro":"<li>En esta aplicación:<ul>",
"cookie_help_step6a_checkbox":"<li>Asegúrese de que la casilla 'Usar cookie' esté marcada.</li>",
"cookie_help_step6b_browse":"<li>Haga clic en el botón 'Explorar...' junto al campo de texto de la cookie.</li>",
"cookie_help_step6c_select":"<li>Seleccione el archivo <code>cookies.txt</code> que acaba de guardar.</li></ul></li>",
"cookie_help_alternative_paste":"<p>Alternativamente, algunas extensiones pueden permitirle copiar la cadena de cookies directamente. Si es así, puede pegarla en el campo de texto en lugar de buscar un archivo.</p>",
"cookie_help_proceed_without_button":"Descargar sin cookies",
"empty_popup_button_tooltip_text": "Abrir Selección de Creador (Explorar creators.json)",
"cookie_help_cancel_download_button":"Cancelar descarga",
"character_input_tooltip":"Introduzca los nombres de los personajes (separados por comas). Admite agrupamiento avanzado y afecta a la nomenclatura de las carpetas si 'Carpetas separadas' está habilitado.\n\nEjemplos:\n- Nami → Coincide con 'Nami', crea la carpeta 'Nami'.\n- (Ulti, Vivi) → Coincide con cualquiera de los dos, carpeta 'Ulti Vivi', añade ambos a Known.txt por separado.\n- (Boa, Hancock)~ → Coincide con cualquiera de los dos, carpeta 'Boa Hancock', añade como un grupo en Known.txt.\n\nLos nombres se tratan como alias para la coincidencia.\n\nModos de filtro (el botón alterna):\n- Archivos: Filtra por nombre de archivo.\n- Título: Filtra por título de la publicación.\n- Ambos: Primero el título, luego el nombre del archivo.\n- Comentarios (Beta): Primero el nombre del archivo, luego los comentarios de la publicación.",
"tour_dialog_title":"¡Bienvenido a Kemono Downloader!",
"tour_dialog_never_show_checkbox":"No volver a mostrar este recorrido",
"tour_dialog_skip_button":"Omitir recorrido",
"tour_dialog_back_button":"Atrás",
"tour_dialog_next_button":"Siguiente",
"tour_dialog_finish_button":"Finalizar",
"tour_dialog_step1_title":"👋 ¡Bienvenido!",
"tour_dialog_step1_content":"¡Hola! Este rápido recorrido le guiará por las principales funciones de Kemono Downloader, incluidas las actualizaciones recientes como el filtrado mejorado, las mejoras del modo manga y la gestión de cookies.\n<ul>\n<li>Mi objetivo es ayudarle a descargar fácilmente contenido de <b>Kemono</b> y <b>Coomer</b>.</li><br>\n<li><b>🎨 Botón de selección de creador:</b> Junto a la entrada de URL, haga clic en el icono de la paleta para abrir un cuadro de diálogo. Explore y seleccione creadores de su archivo <code>creators.json</code> para añadir rápidamente sus nombres a la entrada de URL.</li><br>\n<li><b>Consejo importante: ¿La aplicación '(No responde)'?</b><br>\nDespués de hacer clic en 'Iniciar descarga', especialmente para feeds de creadores grandes o con muchos hilos, la aplicación puede mostrarse temporalmente como '(No responde)'. Su sistema operativo (Windows, macOS, Linux) podría incluso sugerirle 'Finalizar proceso' o 'Forzar salida'.<br>\n<b>¡Por favor, sea paciente!</b> La aplicación a menudo sigue trabajando duro en segundo plano. Antes de forzar el cierre, intente comprobar la 'Ubicación de descarga' elegida en su explorador de archivos. Si ve que se están creando nuevas carpetas o que aparecen archivos, significa que la descarga está progresando correctamente. Dele algo de tiempo para que vuelva a responder.</li><br>\n<li>Use los botones <b>Siguiente</b> y <b>Atrás</b> para navegar.</li><br>\n<li>Muchas opciones tienen información sobre herramientas si pasa el ratón sobre ellas para obtener más detalles.</li><br>\n<li>Haga clic en <b>Omitir recorrido</b> para cerrar esta guía en cualquier momento.</li><br>\n<li>Marque <b>'No volver a mostrar este recorrido'</b> si no quiere verlo en futuros inicios.</li>\n</ul>",
"tour_dialog_step2_title":"① Primeros pasos",
"tour_dialog_step2_content":"Comencemos con lo básico para la descarga:\n<ul>\n<li><b>🔗 URL del creador/publicación de Kemono:</b><br>\nPegue la dirección web completa (URL) de la página de un creador (p. ej., <i>https://kemono.su/patreon/user/12345</i>)\no de una publicación específica (p. ej., <i>.../post/98765</i>).<br>\no de un creador de Coomer (p. ej., <i>https://coomer.su/onlyfans/user/artistname</i>)</li><br>\n<li><b>📁 Ubicación de descarga:</b><br>\nHaga clic en 'Explorar...' para elegir una carpeta en su ordenador donde se guardarán todos los archivos descargados.\nEste campo es obligatorio a menos que esté usando el modo 'Solo enlaces'.</li><br>\n<li><b>📄 Rango de páginas (solo URL de creador):</b><br>\nSi descarga desde la página de un creador, puede especificar un rango de páginas para obtener (p. ej., de la 2 a la 5). \nDéjelo en blanco para todas las páginas. Esto está desactivado para URL de publicaciones únicas o cuando el <b>Modo Manga/Cómic</b> está activo.</li>\n</ul>",
"tour_dialog_step3_title":"② Filtrado de descargas",
"tour_dialog_step3_content":"Refine lo que descarga con estos filtros (la mayoría están desactivados en los modos 'Solo enlaces' o 'Solo archivos comprimidos'):\n<ul>\n<li><b>🎯 Filtrar por personaje(s):</b><br>\nIntroduzca los nombres de los personajes, separados por comas (p. ej., <i>Tifa, Aerith</i>). Agrupe alias para un nombre de carpeta combinado: <i>(alias1, alias2, alias3)</i> se convierte en la carpeta 'alias1 alias2 alias3' (después de la limpieza). Todos los nombres del grupo se utilizan como alias para la coincidencia.<br>\nEl botón <b>'Filtro: [Tipo]'</b> (junto a esta entrada) alterna cómo se aplica este filtro:\n<ul><li><i>Filtro: Archivos:</i> Comprueba los nombres de los archivos individuales. Una publicación se conserva si algún archivo coincide; solo se descargan los archivos coincidentes. La nomenclatura de carpetas utiliza el personaje del nombre del archivo coincidente (si 'Carpetas separadas' está activado).</li><br>\n<li><i>Filtro: Título:</i> Comprueba los títulos de las publicaciones. Se descargan todos los archivos de una publicación coincidente. La nomenclatura de carpetas utiliza el personaje del título de la publicación coincidente.</li>\n<li><b>⤵️ Botón Añadir al filtro (Nombres conocidos):</b> Junto al botón 'Añadir' para Nombres conocidos (ver Paso 5), esto abre una ventana emergente. Seleccione nombres de su lista <code>Known.txt</code> mediante casillas de verificación (con una barra de búsqueda) para añadirlos rápidamente al campo 'Filtrar por personaje(s)'. Los nombres agrupados como <code>(Boa, Hancock)</code> de Known.txt se añadirán como <code>(Boa, Hancock)~</code> al filtro.</li><br>\n<li><i>Filtro: Ambos:</i> Comprueba primero el título de la publicación. Si coincide, se descargan todos los archivos. Si no, comprueba los nombres de los archivos y solo se descargan los archivos coincidentes. La nomenclatura de carpetas prioriza la coincidencia del título, luego la coincidencia del archivo.</li><br>\n<li><i>Filtro: Comentarios (Beta):</i> Comprueba primero los nombres de los archivos. Si un archivo coincide, se descargan todos los archivos de la publicación. Si no hay coincidencia de archivo, comprueba los comentarios de la publicación. Si un comentario coincide, se descargan todos los archivos. (Usa más solicitudes de API). La nomenclatura de carpetas prioriza la coincidencia del archivo, luego la coincidencia del comentario.</li></ul>\nEste filtro también influye en la nomenclatura de las carpetas si 'Carpetas separadas por Nombre/Título' está habilitado.</li><br>\n<li><b>🚫 Omitir con palabras:</b><br>\nIntroduzca palabras, separadas por comas (p. ej., <i>WIP, sketch, preview</i>).\nEl botón <b>'Ámbito: [Tipo]'</b> (junto a esta entrada) alterna cómo se aplica este filtro:\n<ul><li><i>Ámbito: Archivos:</i> Omite archivos si sus nombres contienen alguna de estas palabras.</li><br>\n<li><i>Ámbito: Publicaciones:</i> Omite publicaciones completas si sus títulos contienen alguna de estas palabras.</li><br>\n<li><i>Ámbito: Ambos:</i> Aplica tanto la omisión de archivos como de títulos de publicaciones (primero la publicación, luego los archivos).</li></ul></li><br>\n<li><b>Filtrar archivos (Botones de opción):</b> Elija qué descargar:\n<ul>\n<li><i>Todo:</i> Descarga todos los tipos de archivos encontrados.</li><br>\n<li><i>Imágenes/GIF:</i> Solo formatos de imagen comunes y GIF.</li><br>\n<li><i>Vídeos:</i> Solo formatos de vídeo comunes.</li><br>\n<li><b><i>📦 Solo archivos comprimidos:</i></b> Descarga exclusivamente archivos <b>.zip</b> y <b>.rar</b>. Cuando se selecciona, las casillas de verificación 'Omitir .zip' y 'Omitir .rar' se desactivan y desmarcan automáticamente. 'Mostrar enlaces externos' también se desactiva.</li><br>\n<li><i>🎧 Solo audio:</i> Solo formatos de audio comunes (MP3, WAV, FLAC, etc.).</li><br>\n<li><i>🔗 Solo enlaces:</i> Extrae y muestra enlaces externos de las descripciones de las publicaciones en lugar de descargar archivos. Las opciones relacionadas con la descarga y 'Mostrar enlaces externos' se desactivan.</li>\n</ul></li>\n</ul>",
"tour_dialog_step4_title":"③ Modo Favoritos (Descarga alternativa)",
"tour_dialog_step4_content":"La aplicación ofrece un 'Modo Favoritos' para descargar contenido de artistas que ha añadido a favoritos en Kemono.su.\n<ul>\n<li><b>⭐ Casilla de verificación Modo Favoritos:</b><br>\nSituada junto al botón de opción '🔗 Solo enlaces'. Marque esta casilla para activar el Modo Favoritos.</li><br>\n<li><b>Qué sucede en el Modo Favoritos:</b>\n<ul><li>El área de entrada '🔗 URL del creador/publicación de Kemono' se reemplaza por un mensaje que indica que el Modo Favoritos está activo.</li><br>\n<li>Los botones estándar 'Iniciar descarga', 'Pausa', 'Cancelar' se reemplazan por los botones '🖼️ Artistas favoritos' y '📄 Publicaciones favoritas' (Nota: 'Publicaciones favoritas' está previsto para el futuro).</li><br>\n<li>La opción '🍪 Usar cookie' se activa y bloquea automáticamente, ya que se requieren cookies para obtener sus favoritos.</li></ul></li><br>\n<li><b>🖼️ Botón Artistas favoritos:</b><br>\nHaga clic aquí para abrir un cuadro de diálogo que enumera a sus artistas favoritos de Kemono.su. Puede seleccionar uno o más artistas para descargar.</li><br>\n<li><b>Ámbito de descarga de favoritos (Botón):</b><br>\nEste botón (junto a 'Publicaciones favoritas') controla dónde se descargan los favoritos seleccionados:\n<ul><li><i>Ámbito: Ubicación seleccionada:</i> Todos los artistas seleccionados se descargan en la 'Ubicación de descarga' principal que ha establecido. Los filtros se aplican globalmente.</li><br>\n<li><i>Ámbito: Carpetas de artistas:</i> Se crea una subcarpeta (con el nombre del artista) en su 'Ubicación de descarga' principal para cada artista seleccionado. El contenido de ese artista va a su carpeta específica. Los filtros se aplican dentro de la carpeta de cada artista.</li></ul></li><br>\n<li><b>Filtros en el Modo Favoritos:</b><br>\nLas opciones 'Filtrar por personaje(s)', 'Omitir con palabras' y 'Filtrar archivos' siguen aplicándose al contenido descargado de sus artistas favoritos seleccionados.</li>\n</ul>",
"tour_dialog_step5_title":"④ Ajuste fino de las descargas",
"tour_dialog_step5_content":"Más opciones para personalizar sus descargas:\n<ul>\n<li><b>Omitir .zip / Omitir .rar:</b> Marque estas casillas para evitar descargar estos tipos de archivos de archivado.\n<i>(Nota: Están desactivadas e ignoradas si se selecciona el modo de filtro '📦 Solo archivos comprimidos').</i></li><br>\n<li><b>✂️ Eliminar palabras del nombre:</b><br>\nIntroduzca palabras, separadas por comas (p. ej., <i>patreon, [HD]</i>), para eliminarlas de los nombres de los archivos descargados (no distingue mayúsculas y minúsculas).</li><br>\n<li><b>Descargar solo miniaturas:</b> Descarga pequeñas imágenes de vista previa en lugar de archivos de tamaño completo (si están disponibles).</li><br>\n<li><b>Comprimir imágenes grandes:</b> Si la biblioteca 'Pillow' está instalada, las imágenes de más de 1.5MB se convertirán a formato WebP si la versión WebP es significativamente más pequeña.</li><br>\n<li><b>🗄️ Nombre de carpeta personalizado (Solo publicación única):</b><br>\nSi está descargando una URL de publicación específica Y 'Carpetas separadas por Nombre/Título' está habilitado,\npuede introducir un nombre personalizado aquí para la carpeta de descarga de esa publicación.</li><br>\n<li><b>🍪 Usar cookie:</b> Marque esta casilla para usar cookies para las solicitudes. Puede:\n<ul><li>Introducir una cadena de cookies directamente en el campo de texto (p. ej., <i>nombre1=valor1; nombre2=valor2</i>).</li><br>\n<li>Hacer clic en 'Explorar...' para seleccionar un archivo <i>cookies.txt</i> (formato Netscape). La ruta aparecerá en el campo de texto.</li></ul>\nEsto es útil para acceder a contenido que requiere inicio de sesión. El campo de texto tiene prioridad si se rellena.\nSi 'Usar cookie' está marcado pero tanto el campo de texto como el archivo explorado están vacíos, intentará cargar 'cookies.txt' desde el directorio de la aplicación.</li>\n</ul>",
"tour_dialog_step6_title":"⑤ Organización y rendimiento",
"tour_dialog_step6_content":"Organice sus descargas y gestione el rendimiento:\n<ul>\n<li><b>⚙️ Carpetas separadas por Nombre/Título:</b> Crea subcarpetas basadas en la entrada 'Filtrar por personaje(s)' o en los títulos de las publicaciones (puede usar la lista <b>Known.txt</b> como respaldo para los nombres de las carpetas).</li><br>\n<li><b>Subcarpeta por publicación:</b> Si 'Carpetas separadas' está activado, esto crea una subcarpeta adicional para <i>cada publicación individual</i> dentro de la carpeta principal del personaje/título.</li><br>\n<li><b>🚀 Usar multihilo (Hilos):</b> Activa operaciones más rápidas. El número en la entrada 'Hilos' significa:\n<ul><li>Para <b>Feeds de creadores:</b> Número de publicaciones a procesar simultáneamente. Los archivos dentro de cada publicación son descargados secuencialmente por su trabajador (a menos que esté activada la nomenclatura de manga 'Basado en la fecha', que fuerza a 1 trabajador por publicación).</li><br>\n<li>Para <b>URL de publicaciones únicas:</b> Número de archivos a descargar simultáneamente de esa única publicación.</li></ul>\nSi no está marcado, se usa 1 hilo. Un número elevado de hilos (p. ej., >40) puede mostrar una advertencia.</li><br>\n<li><b>Conmutador de descarga multihilo (esquina superior derecha del área de registro):</b><br>\nEl botón <b>'Multihilo: [ON/OFF]'</b> permite activar/desactivar las descargas multisegmento para archivos grandes individuales.\n<ul><li><b>ON:</b> Puede acelerar las descargas de archivos grandes (p. ej., vídeos) pero puede aumentar la intermitencia de la UI o el spam en el registro con muchos archivos pequeños. Al activarlo aparece una advertencia. Si una descarga multihilo falla, se reintenta como una transmisión única.</li><br>\n<li><b>OFF (Predeterminado):</b> Los archivos se descargan en una sola transmisión.</li></ul>\nEsto se desactiva si está activo el modo 'Solo enlaces' o 'Solo archivos comprimidos'.</li><br>\n<li><b>📖 Modo Manga/Cómic (solo URL de creador):</b> Diseñado para contenido secuencial.\n<ul>\n<li>Descarga las publicaciones de la <b>más antigua a la más nueva</b>.</li><br>\n<li>La entrada 'Rango de páginas' se desactiva ya que se obtienen todas las publicaciones.</li><br>\n<li>Un <b>botón de conmutación de estilo de nombre de archivo</b> (p. ej., 'Nombre: Título de la publicación') aparece en la esquina superior derecha del área de registro cuando este modo está activo para un feed de creador. Haga clic en él para alternar entre los estilos de nomenclatura:\n<ul>\n<li><b><i>Nombre: Título de la publicación (Predeterminado):</i></b> El primer archivo de una publicación se nombra según el título limpio de la publicación (p. ej., 'Mi capítulo 1.jpg'). Los archivos posteriores dentro de la *misma publicación* intentarán conservar sus nombres de archivo originales (p. ej., 'page_02.png', 'bonus_art.jpg'). Si la publicación solo tiene un archivo, se nombra según el título de la publicación. Esto generalmente se recomienda para la mayoría de los mangas/cómics.</li><br>\n<li><b><i>Nombre: Archivo original:</i></b> Todos los archivos intentan conservar sus nombres de archivo originales. Se puede introducir un prefijo opcional (p. ej., 'MiSerie_') en el campo de entrada que aparece junto al botón de estilo. Ejemplo: 'MiSerie_ArchivoOriginal.jpg'.</li><br>\n<li><b><i>Nombre: Título+Núm.G. (Título de la publicación + Numeración global):</i></b> Todos los archivos de todas las publicaciones en la sesión de descarga actual se nombran secuencialmente usando el título limpio de la publicación como prefijo, seguido de un contador global. Por ejemplo: Publicación 'Capítulo 1' (2 archivos) -> 'Capítulo 1_001.jpg', 'Capítulo 1_002.png'. La siguiente publicación, 'Capítulo 2' (1 archivo), continuaría la numeración -> 'Capítulo 2_003.jpg'. El multihilo para el procesamiento de publicaciones se desactiva automáticamente para este estilo para garantizar una numeración global correcta.</li><br>\n<li><b><i>Nombre: Basado en la fecha:</i></b> Los archivos se nombran secuencialmente (001.ext, 002.ext, ...) según el orden de publicación de los posts. Se puede introducir un prefijo opcional (p. ej., 'MiSerie_') en el campo de entrada que aparece junto al botón de estilo. Ejemplo: 'MiSerie_001.jpg'. El multihilo para el procesamiento de publicaciones se desactiva automáticamente para este estilo.</li>\n</ul>\n</li><br>\n<li>Para obtener los mejores resultados con los estilos 'Nombre: Título de la publicación', 'Nombre: Título+Núm.G.' o 'Nombre: Basado en la fecha', use el campo 'Filtrar por personaje(s)' con el título del manga/serie para la organización de las carpetas.</li>\n</ul></li><br>\n<li><b>🎭 Known.txt para una organización de carpetas inteligente:</b><br>\n<code>Known.txt</code> (en el directorio de la aplicación) permite un control detallado sobre la organización automática de carpetas cuando 'Carpetas separadas por Nombre/Título' está activado.\n<ul>\n<li><b>Cómo funciona:</b> Cada línea de <code>Known.txt</code> es una entrada.\n<ul><li>Una línea simple como <code>Mi increíble serie</code> significa que el contenido que coincida con esto irá a una carpeta llamada \"Mi increíble serie\".</li><br>\n<li>Una línea agrupada como <code>(Personaje A, Pers A, Nombre Alt A)</code> significa que el contenido que coincida con \"Personaje A\", \"Pers A\" O \"Nombre Alt A\" irá TODO a una única carpeta llamada \"Personaje A Pers A Nombre Alt A\" (después de la limpieza). Todos los términos entre paréntesis se convierten en alias para esa carpeta.</li></ul></li>\n<li><b>Respaldo inteligente:</b> Cuando 'Carpetas separadas por Nombre/Título' está activado, y si una publicación no coincide con ninguna entrada específica de 'Filtrar por personaje(s)', el descargador consulta <code>Known.txt</code> para encontrar un nombre principal coincidente para la creación de la carpeta.</li><br>\n<li><b>Gestión fácil de usar:</b> Añada nombres simples (no agrupados) a través de la lista de la UI a continuación. Para una edición avanzada (como crear/modificar alias agrupados), haga clic en <b>'Abrir Known.txt'</b> para editar el archivo en su editor de texto. La aplicación lo recarga en el siguiente uso o inicio.</li>\n</ul>\n</li>\n</ul>",
"tour_dialog_step7_title":"⑥ Errores comunes y solución de problemas",
"tour_dialog_step7_content":"A veces, las descargas pueden encontrar problemas. Aquí hay algunos comunes:\n<ul>\n<li><b>Información sobre herramientas de entrada de personaje:</b><br>\nIntroduzca los nombres de los personajes, separados por comas (p. ej., <i>Tifa, Aerith</i>).<br>\nAgrupe alias para un nombre de carpeta combinado: <i>(alias1, alias2, alias3)</i> se convierte en la carpeta 'alias1 alias2 alias3'.<br>\nTodos los nombres del grupo se utilizan como alias para el contenido coincidente.<br><br>\nEl botón 'Filtro: [Tipo]' junto a esta entrada alterna cómo se aplica este filtro:<br>\n- Filtro: Archivos: Comprueba los nombres de los archivos individuales. Solo se descargan los archivos coincidentes.<br>\n- Filtro: Título: Comprueba los títulos de las publicaciones. Se descargan todos los archivos de una publicación coincidente.<br>\n- Filtro: Ambos: Comprueba primero el título de la publicación. Si no hay coincidencia, comprueba los nombres de los archivos.<br>\n- Filtro: Comentarios (Beta): Comprueba primero los nombres de los archivos. Si no hay coincidencia, comprueba los comentarios de la publicación.<br><br>\nEste filtro también influye en la nomenclatura de las carpetas si 'Carpetas separadas por Nombre/Título' está habilitado.</li><br>\n<li><b>502 Bad Gateway / 503 Service Unavailable / 504 Gateway Timeout:</b><br>\nEstos generalmente indican problemas temporales del lado del servidor con Kemono/Coomer. El sitio puede estar sobrecargado, en mantenimiento o experimentando problemas.<br>\n<b>Solución:</b> Espere un poco (p. ej., de 30 minutos a unas pocas horas) y vuelva a intentarlo más tarde. Compruebe el sitio directamente en su navegador.</li><br>\n<li><b>Conexión perdida / Conexión rechazada / Tiempo de espera (durante la descarga de archivos):</b><br>\nEsto puede ocurrir debido a su conexión a Internet, inestabilidad del servidor o si el servidor interrumpe la conexión para un archivo grande.<br>\n<b>Solución:</b> Compruebe su conexión a Internet. Intente reducir el número de 'Hilos' si es alto. La aplicación podría solicitarle que reintente algunos archivos fallidos al final de una sesión.</li><br>\n<li><b>Error IncompleteRead:</b><br>\nEl servidor envió menos datos de los esperados. A menudo es un problema de red temporal o un problema del servidor.<br>\n<b>Solución:</b> La aplicación a menudo marcará estos archivos para un intento de reintento al final de la sesión de descarga.</li><br>\n<li><b>403 Prohibido / 401 No autorizado (menos común para publicaciones públicas):</b><br>\nPuede que no tenga permiso para acceder al contenido. Para algunos contenidos de pago o privados, usar la opción 'Usar cookie' con cookies válidas de su sesión de navegador podría ayudar. Asegúrese de que sus cookies estén actualizadas.</li><br>\n<li><b>404 No encontrado:</b><br>\nLa URL de la publicación o del archivo es incorrecta, o el contenido ha sido eliminado del sitio. Vuelva a comprobar la URL.</li><br>\n<li><b>'No se encontraron publicaciones' / 'No se encontró la publicación de destino':</b><br>\nAsegúrese de que la URL sea correcta y que el creador/publicación exista. Si usa rangos de páginas, asegúrese de que sean válidos para el creador. Para publicaciones muy nuevas, puede haber un ligero retraso antes de que aparezcan en la API.</li><br>\n<li><b>Lentitud general / Aplicación '(No responde)':</b><br>\nComo se mencionó en el Paso 1, si la aplicación parece colgarse después de iniciarse, especialmente con feeds de creadores grandes o muchos hilos, por favor, dele tiempo. Es probable que esté procesando datos en segundo plano. Reducir el número de hilos a veces puede mejorar la capacidad de respuesta si esto es frecuente.</li>\n</ul>",
"tour_dialog_step8_title":"⑦ Registro y controles finales",
"tour_dialog_step8_content":"Monitoreo y controles:\n<ul>\n<li><b>📜 Registro de progreso / Registro de enlaces extraídos:</b> Muestra mensajes de descarga detallados. Si el modo '🔗 Solo enlaces' está activo, esta área muestra los enlaces extraídos.</li><br>\n<li><b>Mostrar enlaces externos en el registro:</b> Si se marca, aparecerá un panel de registro secundario debajo del registro principal para mostrar cualquier enlace externo encontrado en las descripciones de las publicaciones. <i>(Esto se desactiva si está activo el modo '🔗 Solo enlaces' o '📦 Solo archivos comprimidos').</i></li><br>\n<li><b>Conmutador de vista de registro (Botón 👁️ / 🙈):</b><br>\nEste botón (esquina superior derecha del área de registro) cambia la vista del registro principal:\n<ul><li><b>👁️ Registro de progreso (Predeterminado):</b> Muestra toda la actividad de descarga, errores y resúmenes.</li><br>\n<li><b>🙈 Registro de personajes omitidos:</b> Muestra una lista de términos clave de los títulos de las publicaciones que se omitieron debido a su configuración de 'Filtrar por personaje(s)'. Útil para identificar contenido que podría estar omitiendo involuntariamente.</li></ul></li><br>\n<li><b>🔄 Reiniciar:</b> Borra todos los campos de entrada, registros y restablece la configuración temporal a sus valores predeterminados. Solo se puede usar cuando no hay ninguna descarga activa.</li><br>\n<li><b>⬇️ Iniciar descarga / 🔗 Extraer enlaces / ⏸️ Pausa / ❌ Cancelar:</b> Estos botones controlan el proceso. 'Cancelar y reiniciar UI' detiene la operación actual y realiza un reinicio suave de la UI, conservando sus entradas de URL y Directorio. 'Pausa/Reanudar' permite detener y continuar temporalmente.</li><br>\n<li>Si algunos archivos fallan con errores recuperables (como 'IncompleteRead'), es posible que se le solicite que los reintente al final de una sesión.</li>\n</ul>\n<br>¡Está todo listo! Haga clic en <b>'Finalizar'</b> para cerrar el recorrido y empezar a usar el descargador.",
"help_guide_dialog_title":"Kemono Downloader - Guía de funciones",
"help_guide_github_tooltip":"Visitar la página de GitHub del proyecto (se abre en el navegador)",
"help_guide_instagram_tooltip":"Visitar nuestra página de Instagram (se abre en el navegador)",
"help_guide_discord_tooltip":"Visitar nuestra comunidad de Discord (se abre en el navegador)",
"help_guide_step1_title":"① Introducción y entradas principales",
"help_guide_step1_content":"<html><head/><body>\n<p>Esta guía ofrece una descripción general de las funciones, campos y botones de Kemono Downloader.</p>\n<h3>Área de entrada principal (arriba a la izquierda)</h3>\n<ul>\n<li><b>🔗 URL del creador/publicación de Kemono:</b>\n<ul>\n<li>Introduzca la dirección web completa de la página de un creador (p. ej., <i>https://kemono.su/patreon/user/12345</i>) o de una publicación específica (p. ej., <i>.../post/98765</i>).</li>\n<li>Admite URL de Kemono (kemono.su, kemono.party) y Coomer (coomer.su, coomer.party).</li>\n</ul>\n</li>\n<li><b>Rango de páginas (de inicio a fin):</b>\n<ul>\n<li>Para URL de creadores: Especifique un rango de páginas para obtener (p. ej., de la 2 a la 5). Déjelo en blanco para todas las páginas.</li>\n<li>Desactivado para URL de publicaciones únicas o cuando el <b>Modo Manga/Cómic</b> está activo.</li>\n</ul>\n</li>\n<li><b>📁 Ubicación de descarga:</b>\n<ul>\n<li>Haga clic en <b>'Explorar...'</b> para elegir una carpeta principal en su ordenador donde se guardarán todos los archivos descargados.</li>\n<li>Este campo es obligatorio a menos que esté usando el modo <b>'🔗 Solo enlaces'</b>.</li>\n</ul>\n</li>\n<li><b>🎨 Botón de selección de creador (junto a la entrada de URL):</b>\n<ul>\n<li>Haga clic en el icono de la paleta (🎨) para abrir el cuadro de diálogo 'Selección de creador'.</li>\n<li>Este cuadro de diálogo carga creadores desde su archivo <code>creators.json</code> (que debe estar en el directorio de la aplicación).</li>\n<li><b>Dentro del cuadro de diálogo:</b>\n<ul>\n<li><b>Barra de búsqueda:</b> Escriba para filtrar la lista de creadores por nombre o servicio.</li>\n<li><b>Lista de creadores:</b> Muestra los creadores de su <code>creators.json</code>. Los creadores que ha añadido a 'favoritos' (en los datos JSON) aparecen en la parte superior.</li>\n<li><b>Casillas de verificación:</b> Seleccione uno o más creadores marcando la casilla junto a su nombre.</li>\n<li><b>Botón 'Ámbito' (p. ej., 'Ámbito: Personajes'):</b> Este botón alterna la organización de la descarga al iniciar descargas desde esta ventana emergente:\n<ul><li><i>Ámbito: Personajes:</i> Las descargas se organizarán en carpetas con nombres de personajes directamente dentro de su 'Ubicación de descarga' principal. Las obras de diferentes creadores para el mismo personaje se agruparán.</li>\n<li><i>Ámbito: Creadores:</i> Las descargas crearán primero una carpeta con el nombre del creador dentro de su 'Ubicación de descarga' principal. Luego, se crearán subcarpetas con nombres de personajes dentro de la carpeta de cada creador.</li></ul>\n</li>\n<li><b>Botón 'Añadir seleccionados':</b> Al hacer clic aquí, se tomarán los nombres de todos los creadores marcados y se añadirán al campo de entrada principal '🔗 URL del creador/publicación de Kemono', separados por comas. El cuadro de diálogo se cerrará.</li>\n</ul>\n</li>\n<li>Esta función proporciona una forma rápida de rellenar el campo de URL para múltiples creadores sin tener que escribir o pegar manualmente cada URL.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step2_title":"② Filtrado de descargas",
"help_guide_step2_content":"<html><head/><body>\n<h3>Filtrado de descargas (panel izquierdo)</h3>\n<ul>\n<li><b>🎯 Filtrar por personaje(s):</b>\n<ul>\n<li>Introduzca nombres, separados por comas (p. ej., <code>Tifa, Aerith</code>).</li>\n<li><b>Alias agrupados para carpeta compartida (entradas separadas en Known.txt):</b> <code>(Vivi, Ulti, Uta)</code>.\n<ul><li>El contenido que coincida con \"Vivi\", \"Ulti\" O \"Uta\" irá a una carpeta compartida llamada \"Vivi Ulti Uta\" (después de la limpieza).</li>\n<li>Si estos nombres son nuevos, se le pedirá que añada \"Vivi\", \"Ulti\" y \"Uta\" como <i>entradas individuales separadas</i> a <code>Known.txt</code>.</li>\n</ul>\n</li>\n<li><b>Alias agrupados para carpeta compartida (entrada única en Known.txt):</b> <code>(Yuffie, Sonon)~</code> (tenga en cuenta la tilde <code>~</code>).\n<ul><li>El contenido que coincida con \"Yuffie\" O \"Sonon\" irá a una carpeta compartida llamada \"Yuffie Sonon\".</li>\n<li>Si es nuevo, se le pedirá que añada \"Yuffie Sonon\" (con los alias Yuffie, Sonon) como una <i>única entrada de grupo</i> a <code>Known.txt</code>.</li>\n</ul>\n</li>\n<li>Este filtro influye en la nomenclatura de las carpetas si 'Carpetas separadas por Nombre/Título' está habilitado.</li>\n</ul>\n</li>\n<li><b>Filtro: Botón [Tipo] (Ámbito del filtro de personajes):</b> Alterna cómo se aplica 'Filtrar por personaje(s)':\n<ul>\n<li><code>Filtro: Archivos</code>: Comprueba los nombres de los archivos individuales. Una publicación se conserva si algún archivo coincide; solo se descargan los archivos coincidentes. La nomenclatura de carpetas utiliza el personaje del nombre del archivo coincidente.</li>\n<li><code>Filtro: Título</code>: Comprueba los títulos de las publicaciones. Se descargan todos los archivos de una publicación coincidente. La nomenclatura de carpetas utiliza el personaje del título de la publicación coincidente.</li>\n<li><code>Filtro: Ambos</code>: Comprueba primero el título de la publicación. Si coincide, se descargan todos los archivos. Si no, comprueba los nombres de los archivos y solo se descargan los archivos coincidentes. La nomenclatura de carpetas prioriza la coincidencia del título, luego la coincidencia del archivo.</li>\n<li><code>Filtro: Comentarios (Beta)</code>: Comprueba primero los nombres de los archivos. Si un archivo coincide, se descargan todos los archivos de la publicación. Si no hay coincidencia de archivo, comprueba los comentarios de la publicación. Si un comentario coincide, se descargan todos los archivos. (Usa más solicitudes de API). La nomenclatura de carpetas prioriza la coincidencia del archivo, luego la coincidencia del comentario.</li>\n</ul>\n</li>\n<li><b>🗄️ Nombre de carpeta personalizado (Solo publicación única):</b>\n<ul>\n<li>Visible y utilizable solo al descargar una URL de publicación específica Y cuando 'Carpetas separadas por Nombre/Título' está habilitado.</li>\n<li>Le permite especificar un nombre personalizado para la carpeta de descarga de esa única publicación.</li>\n</ul>\n</li>\n<li><b>🚫 Omitir con palabras:</b>\n<ul><li>Introduzca palabras, separadas por comas (p. ej., <code>WIP, sketch, preview</code>) para omitir cierto contenido.</li></ul>\n</li>\n<li><b>Ámbito: Botón [Tipo] (Ámbito de las palabras a omitir):</b> Alterna cómo se aplica 'Omitir con palabras':\n<ul>\n<li><code>Ámbito: Archivos</code>: Omite archivos individuales si sus nombres contienen alguna de estas palabras.</li>\n<li><code>Ámbito: Publicaciones</code>: Omite publicaciones completas si sus títulos contienen alguna de estas palabras.</li>\n<li><code>Ámbito: Ambos</code>: Aplica ambos (primero el título de la publicación, luego los archivos individuales).</li>\n</ul>\n</li>\n<li><b>✂️ Eliminar palabras del nombre:</b>\n<ul><li>Introduzca palabras, separadas por comas (p. ej., <code>patreon, [HD]</code>), para eliminarlas de los nombres de los archivos descargados (no distingue mayúsculas y minúsculas).</li></ul>\n</li>\n<li><b>Filtrar archivos (Botones de opción):</b> Elija qué descargar:\n<ul>\n<li><code>Todo</code>: Descarga todos los tipos de archivos encontrados.</li>\n<li><code>Imágenes/GIF</code>: Solo formatos de imagen comunes (JPG, PNG, GIF, WEBP, etc.) y GIF.</li>\n<li><code>Vídeos</code>: Solo formatos de vídeo comunes (MP4, MKV, WEBM, MOV, etc.).</li>\n<li><code>📦 Solo archivos comprimidos</code>: Descarga exclusivamente archivos <b>.zip</b> y <b>.rar</b>. Cuando se selecciona, las casillas de verificación 'Omitir .zip' y 'Omitir .rar' se desactivan y desmarcan automáticamente. 'Mostrar enlaces externos' también se desactiva.</li>\n<li><code>🎧 Solo audio</code>: Descarga solo formatos de audio comunes (MP3, WAV, FLAC, M4A, OGG, etc.). Otras opciones específicas de archivos se comportan como en el modo 'Imágenes' o 'Vídeos'.</li>\n<li><code>🔗 Solo enlaces</code>: Extrae y muestra enlaces externos de las descripciones de las publicaciones en lugar de descargar archivos. Las opciones relacionadas con la descarga y 'Mostrar enlaces externos' se desactivan. El botón de descarga principal cambia a '🔗 Extraer enlaces'.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step3_title":"③ Opciones y configuración de descarga",
"help_guide_step3_content":"<html><head/><body>\n<h3>Opciones y configuración de descarga (panel izquierdo)</h3>\n<ul>\n<li><b>Omitir .zip / Omitir .rar:</b> Casillas de verificación para evitar descargar estos tipos de archivos de archivado. (Desactivadas e ignoradas si se selecciona el modo de filtro '📦 Solo archivos comprimidos').</li>\n<li><b>Descargar solo miniaturas:</b> Descarga pequeñas imágenes de vista previa en lugar de archivos de tamaño completo (si están disponibles).</li>\n<li><b>Comprimir imágenes grandes (a WebP):</b> Si la biblioteca 'Pillow' (PIL) está instalada, las imágenes de más de 1.5MB se convertirán a formato WebP si la versión WebP es significativamente más pequeña.</li>\n<li><b>⚙️ Configuración avanzada:</b>\n<ul>\n<li><b>Carpetas separadas por Nombre/Título:</b> Crea subcarpetas basadas en la entrada 'Filtrar por personaje(s)' o en los títulos de las publicaciones. Puede usar la lista <b>Known.txt</b> como respaldo para los nombres de las carpetas.</li></ul></li></ul></body></html>",
"help_guide_step4_title":"④ Configuración avanzada (Parte 1)",
"help_guide_step4_content":"<html><head/><body><h3>⚙️ Configuración avanzada (continuación)</h3><ul><ul>\n<li><b>Subcarpeta por publicación:</b> Si 'Carpetas separadas' está activado, esto crea una subcarpeta adicional para <i>cada publicación individual</i> dentro de la carpeta principal del personaje/título.</li>\n<li><b>Usar cookie:</b> Marque esta casilla para usar cookies para las solicitudes.\n<ul>\n<li><b>Campo de texto:</b> Introduzca una cadena de cookies directamente (p. ej., <code>nombre1=valor1; nombre2=valor2</code>).</li>\n<li><b>Explorar...:</b> Seleccione un archivo <code>cookies.txt</code> (formato Netscape). La ruta aparecerá en el campo de texto.</li>\n<li><b>Precedencia:</b> El campo de texto (si se rellena) tiene prioridad sobre un archivo explorado. Si 'Usar cookie' está marcado pero ambos están vacíos, intentará cargar <code>cookies.txt</code> desde el directorio de la aplicación.</li>\n</ul>\n</li>\n<li><b>Usar multihilo y entrada de hilos:</b>\n<ul>\n<li>Activa operaciones más rápidas. El número en la entrada 'Hilos' significa:\n<ul>\n<li>Para <b>Feeds de creadores:</b> Número de publicaciones a procesar simultáneamente. Los archivos dentro de cada publicación son descargados secuencialmente por su trabajador (a menos que esté activada la nomenclatura de manga 'Basado en la fecha', que fuerza a 1 trabajador por publicación).</li>\n<li>Para <b>URL de publicaciones únicas:</b> Número de archivos a descargar simultáneamente de esa única publicación.</li>\n</ul>\n</li>\n<li>Si no está marcado, se usa 1 hilo. Un número elevado de hilos (p. ej., >40) puede mostrar una advertencia.</li>\n</ul>\n</li></ul></ul></body></html>",
"help_guide_step5_title":"⑤ Configuración avanzada (Parte 2) y acciones",
"help_guide_step5_content":"<html><head/><body><h3>⚙️ Configuración avanzada (continuación)</h3><ul><ul>\n<li><b>Mostrar enlaces externos en el registro:</b> Si se marca, aparecerá un panel de registro secundario debajo del registro principal para mostrar cualquier enlace externo encontrado en las descripciones de las publicaciones. (Desactivado si está activo el modo '🔗 Solo enlaces' o '📦 Solo archivos comprimidos').</li>\n<li><b>📖 Modo Manga/Cómic (solo URL de creador):</b> Diseñado para contenido secuencial.\n<ul>\n<li>Descarga las publicaciones de la <b>más antigua a la más nueva</b>.</li>\n<li>La entrada 'Rango de páginas' se desactiva ya que se obtienen todas las publicaciones.</li>\n<li>Un <b>botón de conmutación de estilo de nombre de archivo</b> (p. ej., 'Nombre: Título de la publicación') aparece en la esquina superior derecha del área de registro cuando este modo está activo para un feed de creador. Haga clic en él para alternar entre los estilos de nomenclatura:\n<ul>\n<li><code>Nombre: Título de la publicación (Predeterminado)</code>: El primer archivo de una publicación se nombra según el título limpio de la publicación (p. ej., 'Mi capítulo 1.jpg'). Los archivos posteriores dentro de la *misma publicación* intentarán conservar sus nombres de archivo originales (p. ej., 'page_02.png', 'bonus_art.jpg'). Si la publicación solo tiene un archivo, se nombra según el título de la publicación. Esto generalmente se recomienda para la mayoría de los mangas/cómics.</li>\n<li><code>Nombre: Archivo original</code>: Todos los archivos intentan conservar sus nombres de archivo originales.</li>\n<li><code>Nombre: Archivo original</code>: Todos los archivos intentan conservar sus nombres de archivo originales. Cuando este estilo está activo, aparecerá un campo de entrada para un <b>prefijo de nombre de archivo opcional</b> (p. ej., 'MiSerie_') junto a este botón de estilo. Ejemplo: 'MiSerie_ArchivoOriginal.jpg'.</li>\n<li><code>Nombre: Título+Núm.G. (Título de la publicación + Numeración global)</code>: Todos los archivos de todas las publicaciones en la sesión de descarga actual se nombran secuencialmente usando el título limpio de la publicación como prefijo, seguido de un contador global. Ejemplo: Publicación 'Capítulo 1' (2 archivos) -> 'Capítulo 1 001.jpg', 'Capítulo 1 002.png'. Siguiente publicación 'Capítulo 2' (1 archivo) -> 'Capítulo 2 003.jpg'. El multihilo para el procesamiento de publicaciones se desactiva automáticamente para este estilo.</li>\n<li><code>Nombre: Basado en la fecha</code>: Los archivos se nombran secuencialmente (001.ext, 002.ext, ...) según el orden de publicación. Cuando este estilo está activo, aparecerá un campo de entrada para un <b>prefijo de nombre de archivo opcional</b> (p. ej., 'MiSerie_') junto a este botón de estilo. Ejemplo: 'MiSerie_001.jpg'. El multihilo para el procesamiento de publicaciones se desactiva automáticamente para este estilo.</li>\n</ul>\n</li>\n<li>Para obtener los mejores resultados con los estilos 'Nombre: Título de la publicación', 'Nombre: Título+Núm.G.' o 'Nombre: Basado en la fecha', use el campo 'Filtrar por personaje(s)' con el título del manga/serie para la organización de las carpetas.</li>\n</ul>\n</li>\n</ul></li></ul>\n<h3>Botones de acción principales (panel izquierdo)</h3>\n<ul>\n<li><b>⬇️ Iniciar descarga / 🔗 Extraer enlaces:</b> El texto y la función de este botón cambian según la selección del botón de opción 'Filtrar archivos'. Inicia la operación principal.</li>\n<li><b>⏸️ Pausar descarga / ▶️ Reanudar descarga:</b> Le permite detener temporalmente el proceso de descarga/extracción actual y reanudarlo más tarde. Algunas configuraciones de la UI se pueden cambiar mientras está en pausa.</li>\n<li><b>❌ Cancelar y reiniciar UI:</b> Detiene la operación actual y realiza un reinicio suave de la UI. Sus entradas de URL y Directorio de descarga se conservan, pero otras configuraciones y registros se borran.</li>\n</ul></body></html>",
"help_guide_step6_title":"⑥ Lista de espectáculos/personajes conocidos",
"help_guide_step6_content":"<html><head/><body>\n<h3>Gestión de la lista de espectáculos/personajes conocidos (abajo a la izquierda)</h3>\n<p>Esta sección ayuda a gestionar el archivo <code>Known.txt</code>, que se utiliza para la organización inteligente de carpetas cuando 'Carpetas separadas por Nombre/Título' está habilitado, especialmente como respaldo si una publicación no coincide con su entrada activa de 'Filtrar por personaje(s)'.</p>\n<ul>\n<li><b>Abrir Known.txt:</b> Abre el archivo <code>Known.txt</code> (ubicado en el directorio de la aplicación) en su editor de texto predeterminado para una edición avanzada (como crear alias agrupados complejos).</li>\n<li><b>Buscar personajes...:</b> Filtra la lista de nombres conocidos que se muestra a continuación.</li>\n<li><b>Widget de lista:</b> Muestra los nombres principales de su <code>Known.txt</code>. Seleccione entradas aquí para eliminarlas.</li>\n<li><b>Añadir nuevo nombre de espectáculo/personaje (Campo de entrada):</b> Introduzca un nombre o grupo para añadir.\n<ul>\n<li><b>Nombre simple:</b> p. ej., <code>Mi increíble serie</code>. Se añade como una única entrada.</li>\n<li><b>Grupo para entradas separadas en Known.txt:</b> p. ej., <code>(Vivi, Ulti, Uta)</code>. Añade \"Vivi\", \"Ulti\" y \"Uta\" como tres entradas individuales separadas a <code>Known.txt</code>.</li>\n<li><b>Grupo para carpeta compartida y entrada única en Known.txt (Tilde <code>~</code>):</b> p. ej., <code>(Personaje A, Pers A)~</code>. Añade una entrada a <code>Known.txt</code> llamada \"Personaje A Pers A\". \"Personaje A\" y \"Pers A\" se convierten en alias para esta única carpeta/entrada.</li>\n</ul>\n</li>\n<li><b>➕ Botón Añadir:</b> Añade el nombre/grupo del campo de entrada de arriba a la lista y a <code>Known.txt</code>.</li>\n<li><b>⤵️ Botón Añadir al filtro:</b>\n<ul>\n<li>Situado junto al botón '➕ Añadir' para la lista 'Espectáculos/Personajes conocidos'.</li>\n<li>Al hacer clic en este botón se abre una ventana emergente que muestra todos los nombres de su archivo <code>Known.txt</code>, cada uno con una casilla de verificación.</li>\n<li>La ventana emergente incluye una barra de búsqueda para filtrar rápidamente la lista de nombres.</li>\n<li>Puede seleccionar uno o más nombres usando las casillas de verificación.</li>\n<li>Haga clic en 'Añadir seleccionados' para insertar los nombres elegidos en el campo de entrada 'Filtrar por personaje(s)' de la ventana principal.</li>\n<li>Si un nombre seleccionado de <code>Known.txt</code> era originalmente un grupo (p. ej., definido como <code>(Boa, Hancock)</code> en Known.txt), se añadirá al campo de filtro como <code>(Boa, Hancock)~</code>. Los nombres simples se añaden tal cual.</li>\n<li>Para mayor comodidad, en la ventana emergente están disponibles los botones 'Seleccionar todo' y 'Deseleccionar todo'.</li>\n<li>Haga clic en 'Cancelar' para cerrar la ventana emergente sin ningún cambio.</li>\n</ul>\n</li>\n<li><b>🗑️ Botón Eliminar seleccionados:</b> Elimina los nombres seleccionados de la lista y de <code>Known.txt</code>.</li>\n<li><b>❓ Botón (¡este mismo!):</b> Muestra esta completa guía de ayuda.</li>\n</ul></body></html>",
"help_guide_step7_title":"⑦ Área de registro y controles",
"help_guide_step7_content":"<html><head/><body>\n<h3>Área de registro y controles (panel derecho)</h3>\n<ul>\n<li><b>📜 Registro de progreso / Registro de enlaces extraídos (Etiqueta):</b> Título del área de registro principal; cambia si está activo el modo '🔗 Solo enlaces'.</li>\n<li><b>Buscar enlaces... / 🔍 Botón (búsqueda de enlaces):</b>\n<ul><li>Visible solo cuando está activo el modo '🔗 Solo enlaces'. Permite filtrar en tiempo real los enlaces extraídos que se muestran en el registro principal por texto, URL o plataforma.</li></ul>\n</li>\n<li><b>Nombre: Botón [Estilo] (estilo de nombre de archivo de manga):</b>\n<ul><li>Visible solo cuando el <b>Modo Manga/Cómic</b> está activo para un feed de creador y no en el modo 'Solo enlaces' o 'Solo archivos comprimidos'.</li>\n<li>Alterna entre los estilos de nombres de archivo: <code>Título de la publicación</code>, <code>Archivo original</code>, <code>Basado en la fecha</code>. (Consulte la sección Modo Manga/Cómic para más detalles).</li>\n<li>Cuando está activo el estilo 'Archivo original' o 'Basado en la fecha', aparecerá un campo de entrada para un <b>prefijo de nombre de archivo opcional</b> junto a este botón.</li>\n</ul>\n</li>\n<li><b>Multihilo: Botón [ON/OFF]:</b>\n<ul><li>Alterna las descargas multisegmento para archivos grandes individuales.\n<ul><li><b>ON:</b> Puede acelerar las descargas de archivos grandes (p. ej., vídeos) pero puede aumentar la intermitencia de la UI o el spam en el registro con muchos archivos pequeños. Al activarlo aparece una advertencia. Si una descarga multihilo falla, se reintenta como una transmisión única.</li>\n<li><b>OFF (Predeterminado):</b> Los archivos se descargan en una sola transmisión.</li>\n</ul>\n<li>Desactivado si está activo el modo '🔗 Solo enlaces' o '📦 Solo archivos comprimidos'.</li>\n</ul>\n</li>\n<li><b>👁️ / 🙈 Botón (conmutador de vista de registro):</b> Cambia la vista del registro principal:\n<ul>\n<li><b>👁️ Registro de progreso (Predeterminado):</b> Muestra toda la actividad de descarga, errores y resúmenes.</li>\n<li><b>🙈 Registro de personajes omitidos:</b> Muestra una lista de términos clave de los títulos/contenido de las publicaciones que se omitieron debido a su configuración de 'Filtrar por personaje(s)'. Útil para identificar contenido que podría estar omitiendo involuntariamente.</li>\n</ul>\n</li>\n<li><b>🔄 Botón Reiniciar:</b> Borra todos los campos de entrada, registros y restablece la configuración temporal a sus valores predeterminados. Solo se puede usar cuando no hay ninguna descarga activa.</li>\n<li><b>Salida del registro principal (Área de texto):</b> Muestra mensajes de progreso detallados, errores y resúmenes. Si el modo '🔗 Solo enlaces' está activo, esta área muestra los enlaces extraídos.</li>\n<li><b>Salida del registro de personajes omitidos (Área de texto):</b> (Visible mediante el conmutador 👁️ / 🙈) Muestra las publicaciones/archivos omitidos debido a los filtros de personajes.</li>\n<li><b>Salida del registro externo (Área de texto):</b> Aparece debajo del registro principal si se marca 'Mostrar enlaces externos en el registro'. Muestra los enlaces externos encontrados en las descripciones de las publicaciones.</li>\n<li><b>Botón Exportar enlaces:</b>\n<ul><li>Visible y habilitado solo cuando el modo '🔗 Solo enlaces' está activo y se han extraído enlaces.</li>\n<li>Le permite guardar todos los enlaces extraídos en un archivo <code>.txt</code>.</li>\n</ul>\n</li>\n<li><b>Progreso: Etiqueta [Estado]:</b> Muestra el progreso general del proceso de descarga o extracción de enlaces (p. ej., publicaciones procesadas).</li>\n<li><b>Etiqueta de progreso del archivo:</b> Muestra el progreso de las descargas de archivos individuales, incluida la velocidad y el tamaño, o el estado de la descarga multihilo.</li>\n</ul></body></html>",
"help_guide_step8_title":"⑧ Modo Favoritos y futuras funciones",
"help_guide_step8_content":"<html><head/><body>\n<h3>Modo Favoritos (Descarga desde sus favoritos de Kemono.su)</h3>\n<p>Este modo le permite descargar contenido directamente de los artistas que ha añadido a favoritos en Kemono.su.</p>\n<ul>\n<li><b>⭐ Cómo activarlo:</b>\n<ul>\n<li>Marque la casilla <b>'⭐ Modo Favoritos'</b>, situada junto al botón de opción '🔗 Solo enlaces'.</li>\n</ul>\n</li>\n<li><b>Cambios en la UI en el Modo Favoritos:</b>\n<ul>\n<li>El área de entrada '🔗 URL del creador/publicación de Kemono' se reemplaza por un mensaje que indica que el Modo Favoritos está activo.</li>\n<li>Los botones estándar 'Iniciar descarga', 'Pausa', 'Cancelar' se reemplazan por:\n<ul>\n<li>Botón <b>'🖼️ Artistas favoritos'</b></li>\n<li>Botón <b>'📄 Publicaciones favoritas'</b></li>\n</ul>\n</li>\n<li>La opción '🍪 Usar cookie' se activa y bloquea automáticamente, ya que se requieren cookies para obtener sus favoritos.</li>\n</ul>\n</li>\n<li><b>🖼️ Botón Artistas favoritos:</b>\n<ul>\n<li>Al hacer clic aquí se abre un cuadro de diálogo que enumera a todos los artistas que ha añadido a favoritos en Kemono.su.</li>\n<li>Puede seleccionar uno o más artistas de esta lista para descargar su contenido.</li>\n</ul>\n</li>\n<li><b>📄 Botón Publicaciones favoritas (Función futura):</b>\n<ul>\n<li>La descarga de <i>publicaciones</i> específicas añadidas a favoritos (especialmente en un orden secuencial tipo manga si forman parte de una serie) es una función que se encuentra actualmente en desarrollo.</li>\n<li>La mejor manera de gestionar las publicaciones favoritas, especialmente para la lectura secuencial como el manga, todavía se está explorando.</li>\n<li>Si tiene ideas o casos de uso específicos sobre cómo le gustaría descargar y organizar las publicaciones favoritas (p. ej., 'estilo manga' desde los favoritos), considere abrir un issue o unirse a la discusión en la página de GitHub del proyecto. ¡Su opinión es valiosa!</li>\n</ul>\n</li>\n<li><b>Ámbito de descarga de favoritos (botón):</b>\n<ul>\n<li>Este botón (junto a 'Publicaciones favoritas') controla dónde se descarga el contenido de los artistas favoritos seleccionados:\n<ul>\n<li><b><i>Ámbito: Ubicación seleccionada:</i></b> Todos los artistas seleccionados se descargan en la 'Ubicación de descarga' principal que ha establecido en la UI. Los filtros se aplican globalmente a todo el contenido.</li>\n<li><b><i>Ámbito: Carpetas de artistas:</i></b> Para cada artista seleccionado, se crea automáticamente una subcarpeta (con el nombre del artista) dentro de su 'Ubicación de descarga' principal. El contenido de ese artista va a su carpeta específica. Los filtros se aplican dentro de la carpeta dedicada de cada artista.</li>\n</ul>\n</li>\n</ul>\n</li>\n<li><b>Filtros en el Modo Favoritos:</b>\n<ul>\n<li>Las opciones '🎯 Filtrar por personaje(s)', '🚫 Omitir con palabras' y 'Filtrar archivos' que ha establecido en la UI seguirán aplicándose al contenido descargado de sus artistas favoritos seleccionados.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step9_title":"⑨ Archivos clave y recorrido",
"help_guide_step9_content":"<html><head/><body>\n<h3>Archivos clave utilizados por la aplicación</h3>\n<ul>\n<li><b><code>Known.txt</code>:</b>\n<ul>\n<li>Situado en el directorio de la aplicación (donde está el <code>.exe</code> o <code>main.py</code>).</li>\n<li>Almacena su lista de espectáculos, personajes o títulos de series conocidos para la organización automática de carpetas cuando 'Carpetas separadas por Nombre/Título' está habilitado.</li>\n<li><b>Formato:</b>\n<ul>\n<li>Cada línea es una entrada.</li>\n<li><b>Nombre simple:</b> p. ej., <code>Mi increíble serie</code>. El contenido que coincida con esto irá a una carpeta llamada \"Mi increíble serie\".</li>\n<li><b>Alias agrupados:</b> p. ej., <code>(Personaje A, Pers A, Nombre Alt A)</code>. El contenido que coincida con \"Personaje A\", \"Pers A\" O \"Nombre Alt A\" irá TODO a una única carpeta llamada \"Personaje A Pers A Nombre Alt A\" (después de la limpieza). Todos los términos entre paréntesis se convierten en alias para esa carpeta.</li>\n</ul>\n</li>\n<li><b>Uso:</b> Sirve como respaldo para la nomenclatura de carpetas si una publicación no coincide con su entrada activa de 'Filtrar por personaje(s)'. Puede gestionar entradas simples a través de la UI o editar el archivo directamente para alias complejos. La aplicación lo recarga al inicio o en el siguiente uso.</li>\n</ul>\n</li>\n<li><b><code>cookies.txt</code> (Opcional):</b>\n<ul>\n<li>Si usa la función 'Usar cookie' y no proporciona una cadena de cookies directa o no explora un archivo específico, la aplicación buscará un archivo llamado <code>cookies.txt</code> en su directorio.</li>\n<li><b>Formato:</b> Debe estar en formato de archivo de cookies de Netscape.</li>\n<li><b>Uso:</b> Permite que el descargador use la sesión de inicio de sesión de su navegador para acceder a contenido que podría estar detrás de un inicio de sesión en Kemono/Coomer.</li>\n</ul>\n</li>\n</ul>\n<h3>Recorrido para el primer usuario</h3>\n<ul>\n<li>En el primer inicio (o si se reinicia), aparece un cuadro de diálogo de recorrido de bienvenida que le guía por las principales funciones. Puede omitirlo o elegir 'No volver a mostrar este recorrido'.</li>\n</ul>\n<p><em>Muchos elementos de la UI también tienen información sobre herramientas que aparece cuando pasa el ratón sobre ellos, proporcionando pistas rápidas.</em></p>\n</body></html>"
})

translations ["de"]={}
translations ["de"].update ({
"settings_dialog_title":"Einstellungen",
"language_label":"Sprache:",
"lang_english":"Englisch (English)",
"lang_japanese":"Japanisch (日本語)",
"theme_toggle_light":"In den hellen Modus wechseln",
"theme_toggle_dark":"In den dunklen Modus wechseln",
"theme_tooltip_light":"Das Erscheinungsbild der Anwendung auf hell ändern.",
"theme_tooltip_dark":"Das Erscheinungsbild der Anwendung auf dunkel ändern.",
"ok_button":"OK",
"appearance_group_title":"Erscheinungsbild",
"language_group_title":"Spracheinstellungen",
"creator_post_url_label":"🔗 Kemono Ersteller/Beitrags-URL:",
"download_location_label":"📁 Download-Speicherort:",
"filter_by_character_label":"🎯 Nach Charakter(en) filtern (kommagetrennt):",
"skip_with_words_label":"🚫 Mit Wörtern überspringen (kommagetrennt):",
"remove_words_from_name_label":"✂️ Wörter aus dem Namen entfernen:",
"filter_all_radio":"Alles",
"filter_images_radio":"Bilder/GIFs",
"filter_videos_radio":"Videos",
"filter_archives_radio":"📦 Nur Archive",
"filter_links_radio":"🔗 Nur Links",
"filter_audio_radio":"🎧 Nur Audio",
"favorite_mode_checkbox_label":"⭐ Favoritenmodus",
"browse_button_text":"Durchsuchen...",
"char_filter_scope_files_text":"Filter: Dateien",
"char_filter_scope_files_tooltip":"Aktueller Bereich: Dateien\n\nFiltert einzelne Dateien nach Namen. Ein Beitrag wird beibehalten, wenn eine Datei übereinstimmt.\nNur die übereinstimmenden Dateien aus diesem Beitrag werden heruntergeladen.\nBeispiel: Filter 'Tifa'. Die Datei 'Tifa_artwork.jpg' stimmt überein und wird heruntergeladen.\nOrdnerbenennung: Verwendet den Charakter aus dem übereinstimmenden Dateinamen.\n\nKlicken zum Umschalten auf: Beides",
"char_filter_scope_title_text":"Filter: Titel",
"char_filter_scope_title_tooltip":"Aktueller Bereich: Titel\n\nFiltert ganze Beiträge nach ihrem Titel. Alle Dateien aus einem übereinstimmenden Beitrag werden heruntergeladen.\nBeispiel: Filter 'Aerith'. Der Beitrag mit dem Titel 'Aeriths Garten' stimmt überein; alle seine Dateien werden heruntergeladen.\nOrdnerbenennung: Verwendet den Charakter aus dem übereinstimmenden Beitragstitel.\n\nKlicken zum Umschalten auf: Dateien",
"char_filter_scope_both_text":"Filter: Beides",
"char_filter_scope_both_tooltip":"Aktueller Bereich: Beides (Titel dann Dateien)\n\n1. Überprüft den Beitragstitel: Wenn er übereinstimmt, werden alle Dateien aus dem Beitrag heruntergeladen.\n2. Wenn der Titel nicht übereinstimmt, werden die Dateinamen überprüft: Wenn eine Datei übereinstimmt, wird nur diese Datei heruntergeladen.\nBeispiel: Filter 'Cloud'.\n - Beitrag 'Cloud Strife' (Titelübereinstimmung) -> alle Dateien werden heruntergeladen.\n - Beitrag 'Motorradverfolgung' mit 'Cloud_fenrir.jpg' (Dateiübereinstimmung) -> nur 'Cloud_fenrir.jpg' wird heruntergeladen.\nOrdnerbenennung: Priorisiert Titelübereinstimmung, dann Dateiübereinstimmung.\n\nKlicken zum Umschalten auf: Kommentare",
"char_filter_scope_comments_text":"Filter: Kommentare (Beta)",
"char_filter_scope_comments_tooltip":"Aktueller Bereich: Kommentare (Beta - Zuerst Dateien, dann Kommentare als Fallback)\n\n1. Überprüft Dateinamen: Wenn eine Datei im Beitrag mit dem Filter übereinstimmt, wird der gesamte Beitrag heruntergeladen. Kommentare werden NICHT auf diesen Filterbegriff überprüft.\n2. Wenn keine Datei übereinstimmt, DANN werden die Kommentare des Beitrags überprüft: Wenn ein Kommentar übereinstimmt, wird der gesamte Beitrag heruntergeladen.\nBeispiel: Filter 'Barret'.\n - Beitrag A: Dateien 'Barret_gunarm.jpg', 'other.png'. Die Datei 'Barret_gunarm.jpg' stimmt überein. Alle Dateien aus Beitrag A werden heruntergeladen. Kommentare werden nicht auf 'Barret' überprüft.\n - Beitrag B: Dateien 'dyne.jpg', 'weapon.gif'. Kommentare: '...eine Zeichnung von Barret Wallace...'. Keine Dateiübereinstimmung für 'Barret'. Kommentar stimmt überein. Alle Dateien aus Beitrag B werden heruntergeladen.\nOrdnerbenennung: Priorisiert den Charakter aus der Dateiübereinstimmung, dann aus der Kommentarübereinstimmung.\n\nKlicken zum Umschalten auf: Titel",
"char_filter_scope_unknown_text":"Filter: Unbekannt",
"char_filter_scope_unknown_tooltip":"Aktueller Bereich: Unbekannt\n\nDer Charakterfilterbereich befindet sich in einem unbekannten Zustand. Bitte wechseln oder zurücksetzen.\n\nKlicken zum Umschalten auf: Titel",
"skip_words_input_tooltip":"Geben Sie Wörter, durch Kommas getrennt, ein, um das Herunterladen bestimmter Inhalte zu überspringen (z. B. WIP, Skizze, Vorschau).\n\nDie Schaltfläche 'Bereich: [Typ]' neben dieser Eingabe schaltet um, wie dieser Filter angewendet wird:\n- Bereich: Dateien: Überspringt einzelne Dateien, wenn ihre Namen eines dieser Wörter enthalten.\n- Bereich: Beiträge: Überspringt ganze Beiträge, wenn ihre Titel eines dieser Wörter enthalten.\n- Bereich: Beides: Wendet beides an (zuerst Beitragstitel, dann einzelne Dateien, wenn der Beitragstitel in Ordnung ist).",
"remove_words_input_tooltip":"Geben Sie Wörter, durch Kommas getrennt, ein, die aus den heruntergeladenen Dateinamen entfernt werden sollen (Groß-/Kleinschreibung wird nicht beachtet).\nNützlich zum Bereinigen gängiger Präfixe/Suffixe.\nBeispiel: patreon, kemono, [HD], _final",
"skip_scope_files_text":"Bereich: Dateien",
"skip_scope_files_tooltip":"Aktueller Überspringbereich: Dateien\n\nÜberspringt einzelne Dateien, wenn ihre Namen eines der 'Wörter zum Überspringen' enthalten.\nBeispiel: Wörter zum Überspringen \"WIP, sketch\".\n- Datei \"art_WIP.jpg\" -> ÜBERSPRUNGEN.\n- Datei \"final_art.png\" -> HERUNTERGELADEN (wenn andere Bedingungen erfüllt sind).\n\nDer Beitrag wird weiterhin auf andere nicht übersprungene Dateien überprüft.\nKlicken zum Umschalten auf: Beides",
"skip_scope_posts_text":"Bereich: Beiträge",
"skip_scope_posts_tooltip":"Aktueller Überspringbereich: Beiträge\n\nÜberspringt ganze Beiträge, wenn ihre Titel eines der 'Wörter zum Überspringen' enthalten.\nAlle Dateien aus einem übersprungenen Beitrag werden ignoriert.\nBeispiel: Wörter zum Überspringen \"preview, announcement\".\n- Beitrag \"Aufregende Ankündigung!\" -> ÜBERSPRUNGEN.\n- Beitrag \"Fertige Grafik\" -> VERARBEITET (wenn andere Bedingungen erfüllt sind).\n\nKlicken zum Umschalten auf: Dateien",
"skip_scope_both_text":"Bereich: Beides",
"skip_scope_both_tooltip":"Aktueller Überspringbereich: Beides (Beiträge dann Dateien)\n\n1. Überprüft den Beitragstitel: Wenn der Titel ein Überspringwort enthält, wird der gesamte Beitrag ÜBERSPRUNGEN.\n2. Wenn der Beitragstitel in Ordnung ist, werden die einzelnen Dateinamen überprüft: Wenn ein Dateiname ein Überspringwort enthält, wird nur diese Datei ÜBERSPRUNGEN.\nBeispiel: Wörter zum Überspringen \"WIP, sketch\".\n- Beitrag \"Skizzen und WIPs\" (Titelübereinstimmung) -> GESAMTER BEITRAG ÜBERSPRUNGEN.\n- Beitrag \"Kunst-Update\" (Titel in Ordnung) mit Dateien:\n  - \"character_WIP.jpg\" (Dateiübereinstimmung) -> ÜBERSPRUNGEN.\n  - \"final_scene.png\" (Datei in Ordnung) -> HERUNTERGELADEN.\n\nKlicken zum Umschalten auf: Beiträge",
"skip_scope_unknown_text":"Bereich: Unbekannt",
"skip_scope_unknown_tooltip":"Der Überspringbereich für Wörter befindet sich in einem unbekannten Zustand. Bitte wechseln oder zurücksetzen.\n\nKlicken zum Umschalten auf: Beiträge",
"language_change_title":"Sprache geändert",
"language_change_message":"Die Sprache wurde geändert. Ein Neustart ist erforderlich, damit alle Änderungen vollständig wirksam werden.",
"language_change_informative":"Möchten Sie die Anwendung jetzt neu starten?",
"restart_now_button":"Jetzt neustarten",
"skip_zip_checkbox_label":".zip überspringen",
"skip_rar_checkbox_label":".rar überspringen",
"download_thumbnails_checkbox_label":"Nur Miniaturansichten herunterladen",
"scan_content_images_checkbox_label":"Inhalt nach Bildern durchsuchen",
"compress_images_checkbox_label":"In WebP komprimieren",
"separate_folders_checkbox_label":"Getrennte Ordner nach Name/Titel",
"subfolder_per_post_checkbox_label":"Unterordner pro Beitrag",
"use_cookie_checkbox_label":"Cookie verwenden",
"use_multithreading_checkbox_base_label":"Multithreading verwenden",
"show_external_links_checkbox_label":"Externe Links im Protokoll anzeigen",
"manga_comic_mode_checkbox_label":"Manga/Comic-Modus",
"threads_label":"Threads:",
"start_download_button_text":"⬇️ Download starten",
"start_download_button_tooltip":"Klicken, um den Download- oder Link-Extraktionsprozess mit den aktuellen Einstellungen zu starten.",
"extract_links_button_text":"🔗 Links extrahieren",
"pause_download_button_text":"⏸️ Download anhalten",
"pause_download_button_tooltip":"Klicken, um den laufenden Download-Prozess anzuhalten.",
"resume_download_button_text":"▶️ Download fortsetzen",
"resume_download_button_tooltip":"Klicken, um den Download fortzusetzen.",
"cancel_button_text":"❌ Abbrechen & UI zurücksetzen",
"cancel_button_tooltip":"Klicken, um den laufenden Download-/Extraktionsprozess abzubrechen und die UI-Felder zurückzusetzen (URL und Verzeichnis bleiben erhalten).",
"error_button_text":"Fehler",
"error_button_tooltip":"Dateien anzeigen, die aufgrund von Fehlern übersprungen wurden, und optional erneut versuchen.",
"cancel_retry_button_text":"❌ Wiederholung abbrechen",
"known_chars_label_text":"🎭 Bekannte Shows/Charaktere (für Ordnernamen):",
"open_known_txt_button_text":"Known.txt öffnen",
"known_chars_list_tooltip":"Diese Liste enthält Namen, die für die automatische Ordnererstellung verwendet werden, wenn 'Getrennte Ordner' aktiviert ist\nund kein spezifischer 'Nach Charakter(en) filtern' angegeben oder mit einem Beitrag übereinstimmt.\nFügen Sie Namen von Serien, Spielen oder Charakteren hinzu, die Sie häufig herunterladen.",
"open_known_txt_button_tooltip":"Öffnen Sie die Datei 'Known.txt' in Ihrem Standard-Texteditor.\nDie Datei befindet sich im Verzeichnis der Anwendung.",
"add_char_button_text":"➕ Hinzufügen",
"add_char_button_tooltip":"Fügt den Namen aus dem Eingabefeld zur Liste 'Bekannte Shows/Charaktere' hinzu.",
"add_to_filter_button_text":"⤵️ Zum Filter hinzufügen",
"add_to_filter_button_tooltip":"Wählen Sie Namen aus der Liste 'Bekannte Shows/Charaktere' aus, um sie zum obigen Feld 'Nach Charakter(en) filtern' hinzuzufügen.",
"delete_char_button_text":"🗑️ Ausgewählte löschen",
"delete_char_button_tooltip":"Löscht die ausgewählten Namen aus der Liste 'Bekannte Shows/Charaktere'.",
"progress_log_label_text":"📜 Fortschrittsprotokoll:",
"radio_all_tooltip":"Alle in den Beiträgen gefundenen Dateitypen herunterladen.",
"radio_images_tooltip":"Nur gängige Bildformate (JPG, PNG, GIF, WEBP usw.) herunterladen.",
"radio_videos_tooltip":"Nur gängige Videoformate (MP4, MKV, WEBM, MOV usw.) herunterladen.",
"radio_only_archives_tooltip":"Ausschließlich .zip- und .rar-Dateien herunterladen. Andere dateispezifische Optionen sind deaktiviert.",
"radio_only_audio_tooltip":"Nur gängige Audioformate (MP3, WAV, FLAC usw.) herunterladen.",
"radio_only_links_tooltip":"Externe Links aus Beitragsbeschreibungen extrahieren und anzeigen, anstatt Dateien herunterzuladen.\nDownload-bezogene Optionen werden deaktiviert.",
"favorite_mode_checkbox_tooltip":"Aktivieren Sie den Favoritenmodus, um gespeicherte Künstler/Beiträge zu durchsuchen.\nDies ersetzt die URL-Eingabe durch Favoriten-Auswahlschaltflächen.",
"skip_zip_checkbox_tooltip":"Wenn aktiviert, werden .zip-Archivdateien nicht heruntergeladen.\n(Deaktiviert, wenn 'Nur Archive' ausgewählt ist).",
"skip_rar_checkbox_tooltip":"Wenn aktiviert, werden .rar-Archivdateien nicht heruntergeladen.\n(Deaktiviert, wenn 'Nur Archive' ausgewählt ist).",
"download_thumbnails_checkbox_tooltip":"Lädt kleine Vorschaubilder von der API anstelle von Dateien in voller Größe herunter (falls verfügbar).\nWenn auch 'Beitraginhalt nach Bild-URLs durchsuchen' aktiviert ist, lädt dieser Modus *nur* Bilder herunter, die durch die Inhaltssuche gefunden wurden (API-Miniaturansichten werden ignoriert).",
"scan_content_images_checkbox_tooltip":"Wenn aktiviert, durchsucht der Downloader den HTML-Inhalt von Beiträgen nach Bild-URLs (aus <img>-Tags oder direkten Links).\nDies beinhaltet die Auflösung relativer Pfade aus <img>-Tags in vollständige URLs.\nRelative Pfade in <img>-Tags (z. B. /data/image.jpg) werden in vollständige URLs aufgelöst.\nNützlich in Fällen, in denen Bilder in der Beitragsbeschreibung, aber nicht in der Datei-/Anhangsliste der API enthalten sind.",
"compress_images_checkbox_tooltip":"Bilder > 1,5 MB in das WebP-Format komprimieren (erfordert Pillow).",
"use_subfolders_checkbox_tooltip":"Erstellt Unterordner basierend auf der Eingabe 'Nach Charakter(en) filtern' oder den Beitragstiteln.\nVerwendet die Liste 'Bekannte Shows/Charaktere' als Fallback für Ordnernamen, wenn kein spezifischer Filter übereinstimmt.\nAktiviert die Eingabe 'Nach Charakter(en) filtern' und 'Benutzerdefinierter Ordnername' für einzelne Beiträge.",
"use_subfolder_per_post_checkbox_tooltip":"Erstellt einen Unterordner für jeden Beitrag. Wenn auch 'Getrennte Ordner' aktiviert ist, befindet er sich im Charakter-/Titelordner.",
"use_cookie_checkbox_tooltip":"Wenn aktiviert, wird versucht, Cookies aus 'cookies.txt' (Netscape-Format) zu verwenden\nim Anwendungsverzeichnis für Anfragen.\nNützlich für den Zugriff auf Inhalte, die eine Anmeldung auf Kemono/Coomer erfordern.",
"cookie_text_input_tooltip":"Geben Sie Ihre Cookie-Zeichenfolge direkt ein.\nDiese wird verwendet, wenn 'Cookie verwenden' aktiviert ist UND 'cookies.txt' nicht gefunden wird oder dieses Feld nicht leer ist.\nDas Format hängt davon ab, wie das Backend es analysiert (z. B. 'name1=value1; name2=value2').",
"use_multithreading_checkbox_tooltip":"Aktiviert gleichzeitige Operationen. Siehe die Eingabe 'Threads' für Details.",
"thread_count_input_tooltip":"Anzahl der gleichzeitigen Operationen.\n- Einzelner Beitrag: Gleichzeitige Dateidownloads (1-10 empfohlen).\n- Ersteller-Feed-URL: Anzahl der gleichzeitig zu verarbeitenden Beiträge (1-200 empfohlen).\n  Dateien innerhalb jedes Beitrags werden von seinem Worker nacheinander heruntergeladen.\nWenn 'Multithreading verwenden' nicht aktiviert ist, wird 1 Thread verwendet.",
"external_links_checkbox_tooltip":"Wenn aktiviert, erscheint unter dem Hauptprotokoll ein sekundäres Protokollfenster, um externe Links anzuzeigen, die in Beitragsbeschreibungen gefunden wurden.\n(Deaktiviert, wenn der Modus 'Nur Links' oder 'Nur Archive' aktiv ist).",
"manga_mode_checkbox_tooltip":"Lädt Beiträge vom ältesten zum neuesten herunter und benennt Dateien basierend auf dem Beitragstitel um (nur für Ersteller-Feeds).",
"multipart_on_button_text":"Mehrteilig: EIN",
"multipart_on_button_tooltip":"Mehrteiliger Download: EIN\n\nAktiviert das gleichzeitige Herunterladen großer Dateien in mehreren Segmenten.\n- Kann das Herunterladen einzelner großer Dateien (z. B. Videos) beschleunigen.\n- Kann die CPU-/Netzwerkauslastung erhöhen.\n- Bei Feeds mit vielen kleinen Dateien bietet dies möglicherweise keine Geschwindigkeitsvorteile und könnte die Benutzeroberfläche/das Protokoll überlasten.\n- Wenn der mehrteilige Download fehlschlägt, wird er als Einzelstream wiederholt.\n\nKlicken zum Ausschalten.",
"multipart_off_button_text":"Mehrteilig: AUS",
"multipart_off_button_tooltip":"Mehrteiliger Download: AUS\n\nAlle Dateien werden über einen einzigen Stream heruntergeladen.\n- Stabil und funktioniert in den meisten Szenarien gut, insbesondere bei vielen kleineren Dateien.\n- Große Dateien werden nacheinander heruntergeladen.\n\nKlicken zum Einschalten (siehe Hinweis).",
"reset_button_text":"🔄 Zurücksetzen",
"reset_button_tooltip":"Alle Eingaben und Protokolle auf den Standardzustand zurücksetzen (nur im Leerlauf).",
"progress_idle_text":"Fortschritt: Leerlauf",
"missed_character_log_label_text":"🚫 Protokoll verpasster Charaktere:",
"creator_popup_title":"Erstellerauswahl",
"creator_popup_search_placeholder":"Nach Name, Dienst suchen oder Ersteller-URL einfügen...",
"creator_popup_add_selected_button":"Ausgewählte hinzufügen",
"creator_popup_scope_characters_button":"Bereich: Charaktere",
"creator_popup_scope_creators_button":"Bereich: Ersteller",
"favorite_artists_button_text":"🖼️ Lieblingskünstler",
"favorite_artists_button_tooltip":"Durchsuchen und herunterladen von Ihren Lieblingskünstlern auf Kemono.su/Coomer.su.",
"favorite_posts_button_text":"📄 Lieblingsbeiträge",
"favorite_posts_button_tooltip":"Durchsuchen und herunterladen Ihrer Lieblingsbeiträge von Kemono.su/Coomer.su.",
"favorite_scope_selected_location_text":"Bereich: Ausgewählter Ort",
"favorite_scope_selected_location_tooltip":"Aktueller Favoriten-Download-Bereich: Ausgewählter Ort\n\nAlle ausgewählten Lieblingskünstler/Beiträge werden in den in der Benutzeroberfläche angegebenen Haupt-'Download-Speicherort' heruntergeladen.\nFilter (Charakter, Wörter zum Überspringen, Dateityp) werden global auf alle Inhalte angewendet.\n\nKlicken, um zu ändern auf: Künstlerordner",
"favorite_scope_artist_folders_text":"Bereich: Künstlerordner",
"favorite_scope_artist_folders_tooltip":"Aktueller Favoriten-Download-Bereich: Künstlerordner\n\nFür jeden ausgewählten Lieblingskünstler/Beitrag wird ein neuer Unterordner (benannt nach dem Künstler) im Haupt-'Download-Speicherort' erstellt.\nInhalte für diesen Künstler/Beitrag werden in ihren spezifischen Unterordner heruntergeladen.\nFilter (Charakter, Wörter zum Überspringen, Dateityp) werden *innerhalb* des Ordners jedes Künstlers angewendet.\n\nKlicken, um zu ändern auf: Ausgewählter Ort",
"favorite_scope_unknown_text":"Bereich: Unbekannt",
"favorite_scope_unknown_tooltip":"Der Favoriten-Download-Bereich ist unbekannt. Klicken zum Umschalten.",
"manga_style_post_title_text":"Name: Beitragstitel",
"manga_style_original_file_text":"Name: Originaldatei",
"manga_style_date_based_text":"Name: Datumsbasiert",
"manga_style_title_global_num_text":"Name: Titel+G.Nr.",
"manga_style_unknown_text":"Name: Unbekannter Stil",
"fav_artists_dialog_title":"Lieblingskünstler",
"fav_artists_loading_status":"Lade Lieblingskünstler...",
"fav_artists_search_placeholder":"Künstler suchen...",
"fav_artists_select_all_button":"Alle auswählen",
"fav_artists_deselect_all_button":"Alle abwählen",
"fav_artists_download_selected_button":"Ausgewählte herunterladen",
"fav_artists_cancel_button":"Abbrechen",
"fav_artists_loading_from_source_status":"⏳ Lade Favoriten von {source_name}...",
"fav_artists_found_status":"Insgesamt {count} Lieblingskünstler gefunden.",
"fav_artists_none_found_status":"Keine Lieblingskünstler auf Kemono.su oder Coomer.su gefunden.",
"fav_artists_failed_status":"Fehler beim Abrufen der Favoriten.",
"fav_artists_cookies_required_status":"Fehler: Cookies sind aktiviert, konnten aber für keine Quelle geladen werden.",
"fav_artists_no_favorites_after_processing":"Nach der Verarbeitung wurden keine Lieblingskünstler gefunden.",
"fav_artists_no_selection_title":"Keine Auswahl",
"fav_artists_no_selection_message":"Bitte wählen Sie mindestens einen Künstler zum Herunterladen aus.",
"fav_posts_dialog_title":"Lieblingsbeiträge",
"fav_posts_loading_status":"Lade Lieblingsbeiträge...",
"fav_posts_search_placeholder":"Beiträge suchen (Titel, Ersteller, ID, Dienst)...",
"fav_posts_select_all_button":"Alle auswählen",
"fav_posts_deselect_all_button":"Alle abwählen",
"fav_posts_download_selected_button":"Ausgewählte herunterladen",
"fav_posts_cancel_button":"Abbrechen",
"fav_posts_cookies_required_error":"Fehler: Für Lieblingsbeiträge sind Cookies erforderlich, konnten aber nicht geladen werden.",
"fav_posts_auth_failed_title":"Autorisierungsfehler (Beiträge)",
"fav_posts_auth_failed_message":"Favoriten konnten aufgrund eines Autorisierungsfehlers nicht abgerufen werden{domain_specific_part}:\n\n{error_message}\n\nDies bedeutet normalerweise, dass Ihre Cookies für die Website fehlen, ungültig oder abgelaufen sind. Bitte überprüfen Sie Ihre Cookie-Einstellungen.",
"fav_posts_fetch_error_title":"Abruffehler",
"fav_posts_fetch_error_message":"Fehler beim Abrufen von Favoriten von {domain}{error_message_part}",
"fav_posts_no_posts_found_status":"Keine Lieblingsbeiträge gefunden.",
"fav_posts_found_status":"{count} Lieblingsbeiträge gefunden.",
"fav_posts_display_error_status":"Fehler beim Anzeigen von Beiträgen: {error}",
"fav_posts_ui_error_title":"UI-Fehler",
"fav_posts_ui_error_message":"Lieblingsbeiträge konnten nicht angezeigt werden: {error}",
"fav_posts_auth_failed_message_generic":"Favoriten konnten aufgrund eines Autorisierungsfehlers nicht abgerufen werden{domain_specific_part}. Dies bedeutet normalerweise, dass Ihre Cookies für die Website fehlen, ungültig oder abgelaufen sind. Bitte überprüfen Sie Ihre Cookie-Einstellungen.",
"key_fetching_fav_post_list_init":"Rufe Liste der Lieblingsbeiträge ab...",
"key_fetching_from_source_kemono_su":"Rufe Favoriten von Kemono.su ab...",
"key_fetching_from_source_coomer_su":"Rufe Favoriten von Coomer.su ab...",
"fav_posts_fetch_cancelled_status":"Abruf von Lieblingsbeiträgen abgebrochen.",
"known_names_filter_dialog_title":"Bekannte Namen zum Filter hinzufügen",
"known_names_filter_search_placeholder":"Namen suchen...",
"known_names_filter_select_all_button":"Alle auswählen",
"known_names_filter_deselect_all_button":"Alle abwählen",
"known_names_filter_add_selected_button":"Ausgewählte hinzufügen",
"error_files_dialog_title":"Dateien aufgrund von Fehlern übersprungen",
"error_files_no_errors_label":"In der letzten Sitzung oder nach Wiederholungsversuchen wurden keine Dateien aufgrund von Fehlern als übersprungen protokolliert.",
"error_files_found_label":"Die folgenden {count} Dateien wurden aufgrund von Downloadfehlern übersprungen:",
"error_files_select_all_button":"Alle auswählen",
"error_files_retry_selected_button":"Ausgewählte erneut versuchen",
"error_files_export_urls_button":"URLs in .txt exportieren",
"error_files_no_selection_retry_message":"Bitte wählen Sie mindestens eine Datei zum erneuten Versuch aus.",
"error_files_no_errors_export_title":"Keine Fehler",
"error_files_no_errors_export_message":"Es gibt keine Fehlerdatei-URLs zum Exportieren.",
"error_files_no_urls_found_export_title":"Keine URLs gefunden",
"error_files_no_urls_found_export_message":"Es konnten keine URLs aus der Fehlerdateiliste zum Exportieren extrahiert werden.",
"error_files_save_dialog_title":"Fehlerdatei-URLs speichern",
"error_files_export_success_title":"Export erfolgreich",
"error_files_export_success_message":"{count} Einträge erfolgreich exportiert nach:\n{filepath}",
"error_files_export_error_title":"Exportfehler",
"error_files_export_error_message":"Dateilinks konnten nicht exportiert werden: {error}",
"export_options_dialog_title":"Exportoptionen",
"export_options_description_label":"Wählen Sie das Format für den Export von Fehlerdateilinks:",
"export_options_radio_link_only":"Link pro Zeile (nur URL)",
"export_options_radio_link_only_tooltip":"Exportiert nur die direkte Download-URL für jede fehlgeschlagene Datei, eine URL pro Zeile.",
"export_options_radio_with_details":"Mit Details exportieren (URL [Beitrag, Dateiinfo])",
"export_options_radio_with_details_tooltip":"Exportiert die URL gefolgt von Details wie Beitragstitel, Beitrags-ID und Originaldateiname in Klammern.",
"export_options_export_button":"Exportieren",
"no_errors_logged_title":"Keine Fehler protokolliert",
"no_errors_logged_message":"In der letzten Sitzung oder nach Wiederholungsversuchen wurden keine Dateien aufgrund von Fehlern als übersprungen protokolliert.",
"progress_initializing_text":"Fortschritt: Initialisiere...",
"progress_posts_text":"Fortschritt: {processed_posts} / {total_posts} Beiträge ({progress_percent:.1f}%)",
"progress_processing_post_text":"Fortschritt: Verarbeite Beitrag {processed_posts}...",
"progress_starting_text":"Fortschritt: Starte...",
"downloading_file_known_size_text":"Lade '{filename}' herunter ({downloaded_mb:.1f}MB / {total_mb:.1f}MB)",
"downloading_file_unknown_size_text":"Lade '{filename}' herunter ({downloaded_mb:.1f}MB)",
"downloading_multipart_text":"DL '{filename}...': {downloaded_mb:.1f}/{total_mb:.1f} MB ({parts} Teile @ {speed:.2f} MB/s)",
"downloading_multipart_initializing_text":"Datei: {filename} - Initialisiere Teile...",
"status_completed":"Abgeschlossen",
"status_cancelled_by_user":"Vom Benutzer abgebrochen",
"files_downloaded_label":"heruntergeladen",
"files_skipped_label":"übersprungen",
"retry_finished_text":"Wiederholung abgeschlossen",
"succeeded_text":"Erfolgreich",
"failed_text":"Fehlgeschlagen",
"ready_for_new_task_text":"Bereit für neue Aufgabe.",
"fav_mode_active_label_text":"⭐ Wählen Sie unten Filter aus, bevor Sie Ihre Favoriten auswählen.",
"export_links_button_text":"Links exportieren",
"download_extracted_links_button_text":"Herunterladen",
"download_selected_button_text":"Ausgewählte herunterladen",
"link_input_placeholder_text":"z. B. https://kemono.su/patreon/user/12345 oder .../post/98765",
"link_input_tooltip_text":"Geben Sie die vollständige URL einer Kemono/Coomer-Erstellerseite oder eines bestimmten Beitrags ein.\nBeispiel (Ersteller): https://kemono.su/patreon/user/12345\nBeispiel (Beitrag): https://kemono.su/patreon/user/12345/post/98765",
"dir_input_placeholder_text":"Wählen Sie den Ordner aus, in dem die Downloads gespeichert werden sollen",
"dir_input_tooltip_text":"Geben Sie den Hauptordner ein oder durchsuchen Sie ihn, in dem alle heruntergeladenen Inhalte gespeichert werden.\nDieses Feld ist erforderlich, es sei denn, der Modus 'Nur Links' ist ausgewählt.",
"character_input_placeholder_text":"z. B. Tifa, Aerith, (Cloud, Zack)",
"custom_folder_input_placeholder_text":"Optional: Diesen Beitrag in einem bestimmten Ordner speichern",
"custom_folder_input_tooltip_text":"Wenn Sie eine einzelne Beitrags-URL herunterladen UND 'Getrennte Ordner nach Name/Titel' aktiviert ist,\nkönnen Sie hier einen benutzerdefinierten Namen für den Download-Ordner dieses Beitrags eingeben.\nBeispiel: Meine Lieblingsszene",
"skip_words_input_placeholder_text":"z. B. WM, WIP, sketch, preview",
"remove_from_filename_input_placeholder_text":"z. B. patreon, HD",
"cookie_text_input_placeholder_no_file_selected_text":"Cookie-Zeichenfolge (wenn keine cookies.txt ausgewählt ist)",
"cookie_text_input_placeholder_with_file_selected_text":"Verwende ausgewählte Cookie-Datei (siehe Durchsuchen...)",
"character_search_input_placeholder_text":"Charaktere suchen...",
"character_search_input_tooltip_text":"Tippen Sie hier, um die Liste der bekannten Shows/Charaktere unten zu filtern.",
"new_char_input_placeholder_text":"Neuen Show-/Charakternamen hinzufügen",
"new_char_input_tooltip_text":"Geben Sie einen neuen Show-, Spiel- oder Charakternamen ein, um ihn der obigen Liste hinzuzufügen.",
"link_search_input_placeholder_text":"Links suchen...",
"link_search_input_tooltip_text":"Im Modus 'Nur Links' tippen Sie hier, um die angezeigten Links nach Text, URL oder Plattform zu filtern.",
"manga_date_prefix_input_placeholder_text":"Präfix für Manga-Dateinamen",
"manga_date_prefix_input_tooltip_text":"Optionales Präfix für 'Datumsbasierte' oder 'Originaldatei'-Manga-Dateinamen (z. B. 'Serienname').\nWenn leer, werden die Dateien nach dem Stil ohne Präfix benannt.",
"log_display_mode_links_view_text":"🔗 Link-Ansicht",
"log_display_mode_progress_view_text":"⬇️ Fortschrittsansicht",
"download_external_links_dialog_title":"Ausgewählte externe Links herunterladen",
"select_all_button_text":"Alle auswählen",
"deselect_all_button_text":"Alle abwählen",
"cookie_browse_button_tooltip":"Suchen Sie nach einer Cookie-Datei (Netscape-Format, normalerweise cookies.txt).\nDiese wird verwendet, wenn 'Cookie verwenden' aktiviert ist und das Textfeld oben leer ist.",
"page_range_label_text":"Seitenbereich:",
"start_page_input_placeholder":"Start",
"start_page_input_tooltip":"Für Ersteller-URLs: Geben Sie die Startseitenzahl an, von der heruntergeladen werden soll (z. B. 1, 2, 3).\nLassen Sie das Feld leer oder setzen Sie es auf 1, um von der ersten Seite zu beginnen.\nDeaktiviert für einzelne Beitrags-URLs oder im Manga/Comic-Modus.",
"page_range_to_label_text":"bis",
"end_page_input_placeholder":"Ende",
"end_page_input_tooltip":"Für Ersteller-URLs: Geben Sie die Endseitenzahl an, bis zu der heruntergeladen werden soll (z. B. 5, 10).\nLassen Sie das Feld leer, um alle Seiten von der Startseite herunterzuladen.\nDeaktiviert für einzelne Beitrags-URLs oder im Manga/Comic-Modus.",
"known_names_help_button_tooltip_text":"Öffnen Sie die Anwendungsfunktionsanleitung.",
"future_settings_button_tooltip_text":"Anwendungseinstellungen öffnen (Thema, Sprache usw.).",
"link_search_button_tooltip_text":"Angezeigte Links filtern",
"confirm_add_all_dialog_title":"Hinzufügen neuer Namen bestätigen",
"confirm_add_all_info_label":"Die folgenden neuen Namen/Gruppen aus Ihrer Eingabe 'Nach Charakter(en) filtern' sind nicht in 'Known.txt' enthalten.\nDas Hinzufügen kann die Ordnerorganisation für zukünftige Downloads verbessern.\n\nÜberprüfen Sie die Liste und wählen Sie eine Aktion aus:",
"confirm_add_all_select_all_button":"Alle auswählen",
"confirm_add_all_deselect_all_button":"Alle abwählen",
"confirm_add_all_add_selected_button":"Ausgewählte zu Known.txt hinzufügen",
"confirm_add_all_skip_adding_button":"Dieses Hinzufügen überspringen",
"confirm_add_all_cancel_download_button":"Download abbrechen",
"cookie_help_dialog_title":"Anweisungen zur Cookie-Datei",
"cookie_help_instruction_intro":"<p>Um Cookies zu verwenden, benötigen Sie normalerweise eine <b>cookies.txt</b>-Datei aus Ihrem Browser.</p>",
"cookie_help_how_to_get_title":"<p><b>So erhalten Sie cookies.txt:</b></p>",
"cookie_help_step1_extension_intro":"<li>Installieren Sie die Erweiterung 'Get cookies.txt LOCALLY' für Ihren Chrome-basierten Browser:<br><a href=\"https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc\" style=\"color: #87CEEB;\">Get cookies.txt LOCALLY im Chrome Web Store</a></li>",
"cookie_help_step2_login":"<li>Gehen Sie zur Website (z. B. kemono.su oder coomer.su) und melden Sie sich bei Bedarf an.</li>",
"cookie_help_step3_click_icon":"<li>Klicken Sie auf das Erweiterungssymbol in Ihrer Browser-Symbolleiste.</li>",
"cookie_help_step4_export":"<li>Klicken Sie auf eine 'Exportieren'-Schaltfläche (z. B. \"Exportieren als\", \"cookies.txt exportieren\" - die genaue Formulierung kann je nach Erweiterungsversion variieren).</li>",
"cookie_help_step5_save_file":"<li>Speichern Sie die heruntergeladene <code>cookies.txt</code>-Datei auf Ihrem Computer.</li>",
"cookie_help_step6_app_intro":"<li>In dieser Anwendung:<ul>",
"cookie_help_step6a_checkbox":"<li>Stellen Sie sicher, dass das Kontrollkästchen 'Cookie verwenden' aktiviert ist.</li>",
"cookie_help_step6b_browse":"<li>Klicken Sie auf die Schaltfläche 'Durchsuchen...' neben dem Cookie-Textfeld.</li>",
"cookie_help_step6c_select":"<li>Wählen Sie die gerade gespeicherte <code>cookies.txt</code>-Datei aus.</li></ul></li>",
"cookie_help_alternative_paste":"<p>Alternativ können einige Erweiterungen es Ihnen ermöglichen, die Cookie-Zeichenfolge direkt zu kopieren. In diesem Fall können Sie sie in das Textfeld einfügen, anstatt nach einer Datei zu suchen.</p>",
"cookie_help_proceed_without_button":"Ohne Cookies herunterladen",
"empty_popup_button_tooltip_text": "Autorenauswahl öffnen (creators.json durchsuchen)",
"cookie_help_cancel_download_button":"Download abbrechen",
"character_input_tooltip":"Geben Sie Charakternamen ein (kommagetrennt). Unterstützt erweiterte Gruppierung und beeinflusst die Ordnerbenennung, wenn 'Getrennte Ordner' aktiviert ist.\n\nBeispiele:\n- Nami → Stimmt mit 'Nami' überein, erstellt den Ordner 'Nami'.\n- (Ulti, Vivi) → Stimmt mit einem von beiden überein, Ordner 'Ulti Vivi', fügt beide separat zu Known.txt hinzu.\n- (Boa, Hancock)~ → Stimmt mit einem von beiden überein, Ordner 'Boa Hancock', fügt als eine Gruppe zu Known.txt hinzu.\n\nNamen werden als Aliase für die Übereinstimmung behandelt.\n\nFiltermodi (Schaltfläche schaltet um):\n- Dateien: Filtert nach Dateinamen.\n- Titel: Filtert nach Beitragstitel.\n- Beides: Zuerst Titel, dann Dateiname.\n- Kommentare (Beta): Zuerst Dateiname, dann Kommentare zum Beitrag.",
"tour_dialog_title":"Willkommen bei Kemono Downloader!",
"tour_dialog_never_show_checkbox":"Diese Tour nie wieder anzeigen",
"tour_dialog_skip_button":"Tour überspringen",
"tour_dialog_back_button":"Zurück",
"tour_dialog_next_button":"Weiter",
"tour_dialog_finish_button":"Fertigstellen",
"tour_dialog_step1_title":"👋 Willkommen!",
"tour_dialog_step1_content":"Hallo! Diese schnelle Tour führt Sie durch die Hauptfunktionen des Kemono Downloaders, einschließlich der neuesten Updates wie verbesserter Filterung, Manga-Modus-Verbesserungen und Cookie-Verwaltung.\n<ul>\n<li>Mein Ziel ist es, Ihnen zu helfen, Inhalte von <b>Kemono</b> und <b>Coomer</b> einfach herunterzuladen.</li><br>\n<li><b>🎨 Erstellerauswahl-Schaltfläche:</b> Klicken Sie neben der URL-Eingabe auf das Palettensymbol, um ein Dialogfeld zu öffnen. Durchsuchen und wählen Sie Ersteller aus Ihrer <code>creators.json</code>-Datei aus, um ihre Namen schnell zur URL-Eingabe hinzuzufügen.</li><br>\n<li><b>Wichtiger Tipp: App '(reagiert nicht)'?</b><br>\nNachdem Sie auf 'Download starten' geklickt haben, insbesondere bei großen Ersteller-Feeds oder mit vielen Threads, kann die Anwendung vorübergehend als '(reagiert nicht)' angezeigt werden. Ihr Betriebssystem (Windows, macOS, Linux) schlägt Ihnen möglicherweise sogar vor, den 'Prozess zu beenden' oder 'Beenden zu erzwingen'.<br>\n<b>Bitte haben Sie Geduld!</b> Die App arbeitet oft noch im Hintergrund. Bevor Sie das Schließen erzwingen, versuchen Sie, Ihren gewählten 'Download-Speicherort' in Ihrem Datei-Explorer zu überprüfen. Wenn Sie sehen, dass neue Ordner erstellt werden oder Dateien erscheinen, bedeutet dies, dass der Download korrekt fortgesetzt wird. Geben Sie ihm etwas Zeit, um wieder zu reagieren.</li><br>\n<li>Verwenden Sie die Schaltflächen <b>Weiter</b> und <b>Zurück</b> zum Navigieren.</li><br>\n<li>Viele Optionen haben Tooltips, wenn Sie mit der Maus darüber fahren, um weitere Details zu erhalten.</li><br>\n<li>Klicken Sie jederzeit auf <b>Tour überspringen</b>, um diesen Leitfaden zu schließen.</li><br>\n<li>Aktivieren Sie <b>'Diese Tour nie wieder anzeigen'</b>, wenn Sie sie bei zukünftigen Starts nicht sehen möchten.</li>\n</ul>",
"tour_dialog_step2_title":"① Erste Schritte",
"tour_dialog_step2_content":"Beginnen wir mit den Grundlagen für das Herunterladen:\n<ul>\n<li><b>🔗 Kemono Ersteller/Beitrags-URL:</b><br>\nFügen Sie die vollständige Webadresse (URL) einer Erstellerseite (z. B. <i>https://kemono.su/patreon/user/12345</i>)\noder eines bestimmten Beitrags (z. B. <i>.../post/98765</i>) ein.<br>\noder eines Coomer-Erstellers (z. B. <i>https://coomer.su/onlyfans/user/artistname</i>)</li><br>\n<li><b>📁 Download-Speicherort:</b><br>\nKlicken Sie auf 'Durchsuchen...', um einen Ordner auf Ihrem Computer auszuwählen, in dem alle heruntergeladenen Dateien gespeichert werden.\nDieses Feld ist erforderlich, es sei denn, Sie verwenden den Modus 'Nur Links'.</li><br>\n<li><b>📄 Seitenbereich (nur Ersteller-URL):</b><br>\nWenn Sie von einer Erstellerseite herunterladen, können Sie einen Seitenbereich zum Abrufen angeben (z. B. Seiten 2 bis 5).\nLassen Sie das Feld für alle Seiten leer. Dies ist für einzelne Beitrags-URLs oder wenn der <b>Manga/Comic-Modus</b> aktiv ist, deaktiviert.</li>\n</ul>",
"tour_dialog_step3_title":"② Downloads filtern",
"tour_dialog_step3_content":"Verfeinern Sie, was Sie herunterladen, mit diesen Filtern (die meisten sind im Modus 'Nur Links' oder 'Nur Archive' deaktiviert):\n<ul>\n<li><b>🎯 Nach Charakter(en) filtern:</b><br>\nGeben Sie Charakternamen ein, durch Kommas getrennt (z. B. <i>Tifa, Aerith</i>). Gruppieren Sie Aliase für einen gemeinsamen Ordnernamen: <i>(alias1, alias2, alias3)</i> wird zum Ordner 'alias1 alias2 alias3' (nach der Bereinigung). Alle Namen in der Gruppe werden als Aliase für die Übereinstimmung verwendet.<br>\nDie Schaltfläche <b>'Filter: [Typ]'</b> (neben dieser Eingabe) schaltet um, wie dieser Filter angewendet wird:\n<ul><li><i>Filter: Dateien:</i> Überprüft einzelne Dateinamen. Ein Beitrag wird beibehalten, wenn eine Datei übereinstimmt; nur übereinstimmende Dateien werden heruntergeladen. Die Ordnerbenennung verwendet den Charakter aus dem übereinstimmenden Dateinamen (wenn 'Getrennte Ordner' aktiviert ist).</li><br>\n<li><i>Filter: Titel:</i> Überprüft Beitragstitel. Alle Dateien aus einem übereinstimmenden Beitrag werden heruntergeladen. Die Ordnerbenennung verwendet den Charakter aus dem übereinstimmenden Beitragstitel.</li>\n<li><b>⤵️ Zum Filter hinzufügen-Schaltfläche (Bekannte Namen):</b> Neben der 'Hinzufügen'-Schaltfläche für bekannte Namen (siehe Schritt 5) öffnet dies ein Popup. Wählen Sie Namen aus Ihrer <code>Known.txt</code>-Liste über Kontrollkästchen (mit einer Suchleiste) aus, um sie schnell zum Feld 'Nach Charakter(en) filtern' hinzuzufügen. Gruppierte Namen wie <code>(Boa, Hancock)</code> aus Known.txt werden als <code>(Boa, Hancock)~</code> zum Filter hinzugefügt.</li><br>\n<li><i>Filter: Beides:</i> Überprüft zuerst den Beitragstitel. Wenn er übereinstimmt, werden alle Dateien heruntergeladen. Wenn nicht, werden die Dateinamen überprüft und nur übereinstimmende Dateien heruntergeladen. Die Ordnerbenennung priorisiert die Titelübereinstimmung, dann die Dateiübereinstimmung.</li><br>\n<li><i>Filter: Kommentare (Beta):</i> Überprüft zuerst die Dateinamen. Wenn eine Datei übereinstimmt, werden alle Dateien aus dem Beitrag heruntergeladen. Wenn keine Dateiübereinstimmung vorliegt, werden die Kommentare des Beitrags überprüft. Wenn ein Kommentar übereinstimmt, werden alle Dateien heruntergeladen. (Verwendet mehr API-Anfragen). Die Ordnerbenennung priorisiert die Dateiübereinstimmung, dann die Kommentarübereinstimmung.</li></ul>\nDieser Filter beeinflusst auch die Ordnerbenennung, wenn 'Getrennte Ordner nach Name/Titel' aktiviert ist.</li><br>\n<li><b>🚫 Mit Wörtern überspringen:</b><br>\nGeben Sie Wörter ein, durch Kommas getrennt (z. B. <i>WIP, sketch, preview</i>).\nDie Schaltfläche <b>'Bereich: [Typ]'</b> (neben dieser Eingabe) schaltet um, wie dieser Filter angewendet wird:\n<ul><li><i>Bereich: Dateien:</i> Überspringt Dateien, wenn ihre Namen eines dieser Wörter enthalten.</li><br>\n<li><i>Bereich: Beiträge:</i> Überspringt ganze Beiträge, wenn ihre Titel eines dieser Wörter enthalten.</li><br>\n<li><i>Bereich: Beides:</i> Wendet sowohl das Überspringen von Dateien als auch von Beitragstiteln an (zuerst Beitrag, dann Dateien).</li></ul></li><br>\n<li><b>Dateien filtern (Radioschaltflächen):</b> Wählen Sie aus, was heruntergeladen werden soll:\n<ul>\n<li><i>Alles:</i> Lädt alle gefundenen Dateitypen herunter.</li><br>\n<li><i>Bilder/GIFs:</i> Nur gängige Bildformate und GIFs.</li><br>\n<li><i>Videos:</i> Nur gängige Videoformate.</li><br>\n<li><b><i>📦 Nur Archive:</i></b> Lädt ausschließlich <b>.zip</b>- und <b>.rar</b>-Dateien herunter. Wenn diese Option ausgewählt ist, werden die Kontrollkästchen 'zip überspringen' und '.rar überspringen' automatisch deaktiviert und abgewählt. 'Externe Links anzeigen' wird ebenfalls deaktiviert.</li><br>\n<li><i>🎧 Nur Audio:</i> Nur gängige Audioformate (MP3, WAV, FLAC usw.).</li><br>\n<li><i>🔗 Nur Links:</i> Extrahiert und zeigt externe Links aus Beitragsbeschreibungen an, anstatt Dateien herunterzuladen. Download-bezogene Optionen und 'Externe Links anzeigen' werden deaktiviert.</li>\n</ul></li>\n</ul>",
"tour_dialog_step4_title":"③ Favoritenmodus (alternativer Download)",
"tour_dialog_step4_content":"Die Anwendung bietet einen 'Favoritenmodus' zum Herunterladen von Inhalten von Künstlern, die Sie auf Kemono.su als Favoriten markiert haben.\n<ul>\n<li><b>⭐ Favoritenmodus-Kontrollkästchen:</b><br>\nBefindet sich neben der Radioschaltfläche '🔗 Nur Links'. Aktivieren Sie dieses Kontrollkästchen, um den Favoritenmodus zu aktivieren.</li><br>\n<li><b>Was im Favoritenmodus passiert:</b>\n<ul><li>Der Eingabebereich '🔗 Kemono Ersteller/Beitrags-URL' wird durch eine Meldung ersetzt, die anzeigt, dass der Favoritenmodus aktiv ist.</li><br>\n<li>Die Standard-Schaltflächen 'Download starten', 'Anhalten', 'Abbrechen' werden durch die Schaltflächen '🖼️ Lieblingskünstler' und '📄 Lieblingsbeiträge' ersetzt (Hinweis: 'Lieblingsbeiträge' ist für die Zukunft geplant).</li><br>\n<li>Die Option '🍪 Cookie verwenden' wird automatisch aktiviert und gesperrt, da Cookies zum Abrufen Ihrer Favoriten erforderlich sind.</li></ul></li><br>\n<li><b>🖼️ Lieblingskünstler-Schaltfläche:</b><br>\nKlicken Sie hier, um ein Dialogfeld zu öffnen, das Ihre Lieblingskünstler von Kemono.su auflistet. Sie können einen oder mehrere Künstler zum Herunterladen auswählen.</li><br>\n<li><b>Favoriten-Download-Bereich (Schaltfläche):</b><br>\nDiese Schaltfläche (neben 'Lieblingsbeiträge') steuert, wohin ausgewählte Favoriten heruntergeladen werden:\n<ul><li><i>Bereich: Ausgewählter Ort:</i> Alle ausgewählten Künstler werden in den von Ihnen festgelegten Haupt-'Download-Speicherort' heruntergeladen. Filter werden global angewendet.</li><br>\n<li><i>Bereich: Künstlerordner:</i> Für jeden ausgewählten Künstler wird in Ihrem Haupt-'Download-Speicherort' ein Unterordner (benannt nach dem Künstler) erstellt. Der Inhalt dieses Künstlers wird in seinen spezifischen Ordner verschoben. Filter werden innerhalb des Ordners jedes Künstlers angewendet.</li></ul></li><br>\n<li><b>Filter im Favoritenmodus:</b><br>\nDie Optionen 'Nach Charakter(en) filtern', 'Mit Wörtern überspringen' und 'Dateien filtern' gelten weiterhin für die von Ihren ausgewählten Lieblingskünstlern heruntergeladenen Inhalte.</li>\n</ul>",
"tour_dialog_step5_title":"④ Downloads feinabstimmen",
"tour_dialog_step5_content":"Weitere Optionen zum Anpassen Ihrer Downloads:\n<ul>\n<li><b>.zip überspringen / .rar überspringen:</b> Aktivieren Sie diese Kontrollkästchen, um das Herunterladen dieser Archivdateitypen zu vermeiden.\n<i>(Hinweis: Diese sind deaktiviert und werden ignoriert, wenn der Filtermodus '📦 Nur Archive' ausgewählt ist).</i></li><br>\n<li><b>✂️ Wörter aus dem Namen entfernen:</b><br>\nGeben Sie Wörter, durch Kommas getrennt, ein (z. B. <i>patreon, [HD]</i>), die aus den heruntergeladenen Dateinamen entfernt werden sollen (Groß-/Kleinschreibung wird nicht beachtet).</li><br>\n<li><b>Nur Miniaturansichten herunterladen:</b> Lädt kleine Vorschaubilder anstelle von Dateien in voller Größe herunter (falls verfügbar).</li><br>\n<li><b>Große Bilder komprimieren:</b> Wenn die 'Pillow'-Bibliothek installiert ist, werden Bilder, die größer als 1,5 MB sind, in das WebP-Format konvertiert, wenn die WebP-Version deutlich kleiner ist.</li><br>\n<li><b>🗄️ Benutzerdefinierter Ordnername (nur einzelner Beitrag):</b><br>\nWenn Sie eine einzelne spezifische Beitrags-URL herunterladen UND 'Getrennte Ordner nach Name/Titel' aktiviert ist,\nkönnen Sie hier einen benutzerdefinierten Namen für den Download-Ordner dieses Beitrags eingeben.</li><br>\n<li><b>🍪 Cookie verwenden:</b> Aktivieren Sie dieses Kontrollkästchen, um Cookies für Anfragen zu verwenden. Sie können entweder:\n<ul><li>Eine Cookie-Zeichenfolge direkt in das Textfeld eingeben (z. B. <i>name1=value1; name2=value2</i>).</li><br>\n<li>Auf 'Durchsuchen...' klicken, um eine <i>cookies.txt</i>-Datei (Netscape-Format) auszuwählen. Der Pfad wird im Textfeld angezeigt.</li></ul>\nDies ist nützlich für den Zugriff auf Inhalte, die eine Anmeldung erfordern. Das Textfeld hat Vorrang, wenn es ausgefüllt ist.\nWenn 'Cookie verwenden' aktiviert ist, aber sowohl das Textfeld als auch die durchsuchte Datei leer sind, wird versucht, 'cookies.txt' aus dem Anwendungsverzeichnis zu laden.</li>\n</ul>",
"tour_dialog_step6_title":"⑤ Organisation & Leistung",
"tour_dialog_step6_content":"Organisieren Sie Ihre Downloads und verwalten Sie die Leistung:\n<ul>\n<li><b>⚙️ Getrennte Ordner nach Name/Titel:</b> Erstellt Unterordner basierend auf der Eingabe 'Nach Charakter(en) filtern' oder den Beitragstiteln (kann die <b>Known.txt</b>-Liste als Fallback für Ordnernamen verwenden).</li><br>\n<li><b>Unterordner pro Beitrag:</b> Wenn 'Getrennte Ordner' aktiviert ist, wird für <i>jeden einzelnen Beitrag</i> ein zusätzlicher Unterordner im Hauptordner für den Charakter/Titel erstellt.</li><br>\n<li><b>🚀 Multithreading verwenden (Threads):</b> Aktiviert schnellere Operationen. Die Zahl in der Eingabe 'Threads' bedeutet:\n<ul><li>Für <b>Ersteller-Feeds:</b> Anzahl der gleichzeitig zu verarbeitenden Beiträge. Dateien innerhalb jedes Beitrags werden von seinem Worker nacheinander heruntergeladen (es sei denn, die Manga-Benennung 'Datumsbasiert' ist aktiviert, was 1 Beitrags-Worker erzwingt).</li><br>\n<li>Für <b>einzelne Beitrags-URLs:</b> Anzahl der gleichzeitig von diesem einzelnen Beitrag herunterzuladenden Dateien.</li></ul>\nWenn nicht aktiviert, wird 1 Thread verwendet. Hohe Thread-Zahlen (z. B. >40) können einen Hinweis anzeigen.</li><br>\n<li><b>Mehrteiliger Download-Schalter (oben rechts im Protokollbereich):</b><br>\nDie Schaltfläche <b>'Mehrteilig: [EIN/AUS]'</b> ermöglicht das Aktivieren/Deaktivieren mehrsegmentiger Downloads für einzelne große Dateien.\n<ul><li><b>EIN:</b> Kann das Herunterladen großer Dateien (z. B. Videos) beschleunigen, kann aber die Benutzeroberfläche bei vielen kleinen Dateien ruckeln lassen oder zu Protokoll-Spam führen. Beim Aktivieren wird ein Hinweis angezeigt. Wenn ein mehrteiliger Download fehlschlägt, wird er als Einzelstream wiederholt.</li><br>\n<li><b>AUS (Standard):</b> Dateien werden in einem einzigen Stream heruntergeladen.</li></ul>\nDies ist deaktiviert, wenn der Modus 'Nur Links' oder 'Nur Archive' aktiv ist.</li><br>\n<li><b>📖 Manga/Comic-Modus (nur Ersteller-URL):</b> Speziell für sequentielle Inhalte.\n<ul>\n<li>Lädt Beiträge vom <b>ältesten zum neuesten</b> herunter.</li><br>\n<li>Die Eingabe 'Seitenbereich' ist deaktiviert, da alle Beiträge abgerufen werden.</li><br>\n<li>Eine <b>Schaltfläche zum Umschalten des Dateinamenstils</b> (z. B. 'Name: Beitragstitel') erscheint oben rechts im Protokollbereich, wenn dieser Modus für einen Ersteller-Feed aktiv ist. Klicken Sie darauf, um zwischen den Benennungsstilen zu wechseln:\n<ul>\n<li><b><i>Name: Beitragstitel (Standard):</i></b> Die erste Datei in einem Beitrag wird nach dem bereinigten Titel des Beitrags benannt (z. B. 'Mein Kapitel 1.jpg'). Nachfolgende Dateien im *gleichen Beitrag* versuchen, ihre ursprünglichen Dateinamen beizubehalten (z. B. 'seite_02.png', 'bonus_art.jpg'). Wenn der Beitrag nur eine Datei hat, wird sie nach dem Beitragstitel benannt. Dies wird im Allgemeinen für die meisten Mangas/Comics empfohlen.</li><br>\n<li><b><i>Name: Originaldatei:</i></b> Alle Dateien versuchen, ihre ursprünglichen Dateinamen beizubehalten. Ein optionales Präfix (z. B. 'MeineSerie_') kann in das Eingabefeld eingegeben werden, das neben der Stil-Schaltfläche erscheint. Beispiel: 'MeineSerie_Originaldatei.jpg'.</li><br>\n<li><b><i>Name: Titel+G.Nr. (Beitragstitel + Globale Nummerierung):</i></b> Alle Dateien in allen Beiträgen der aktuellen Download-Sitzung werden sequentiell unter Verwendung des bereinigten Beitragstitels als Präfix benannt, gefolgt von einem globalen Zähler. Beispiel: Beitrag 'Kapitel 1' (2 Dateien) -> 'Kapitel 1_001.jpg', 'Kapitel 1_002.png'. Der nächste Beitrag 'Kapitel 2' (1 Datei) würde die Nummerierung fortsetzen -> 'Kapitel 2_003.jpg'. Multithreading für die Beitragsverarbeitung wird für diesen Stil automatisch deaktiviert, um eine korrekte globale Nummerierung zu gewährleisten.</li><br>\n<li><b><i>Name: Datumsbasiert:</i></b> Dateien werden sequentiell (001.ext, 002.ext, ...) basierend auf der Veröffentlichungsreihenfolge der Beiträge benannt. Ein optionales Präfix (z. B. 'MeineSerie_') kann in das Eingabefeld eingegeben werden, das neben der Stil-Schaltfläche erscheint. Beispiel: 'MeineSerie_001.jpg'. Multithreading für die Beitragsverarbeitung wird für diesen Stil automatisch deaktiviert.</li>\n</ul>\n</li><br>\n<li>Um mit den Stilen 'Name: Beitragstitel', 'Name: Titel+G.Nr.' oder 'Name: Datumsbasiert' die besten Ergebnisse zu erzielen, verwenden Sie das Feld 'Nach Charakter(en) filtern' mit dem Manga-/Serientitel für die Ordnerorganisation.</li>\n</ul></li><br>\n<li><b>🎭 Known.txt für intelligente Ordnerorganisation:</b><br>\n<code>Known.txt</code> (im Anwendungsverzeichnis) ermöglicht eine feinkörnige Steuerung der automatischen Ordnerorganisation, wenn 'Getrennte Ordner nach Name/Titel' aktiviert ist.\n<ul>\n<li><b>Funktionsweise:</b> Jede Zeile in <code>Known.txt</code> ist ein Eintrag.\n<ul><li>Eine einfache Zeile wie <code>Meine tolle Serie</code> bedeutet, dass Inhalte, die damit übereinstimmen, in einen Ordner namens \"Meine tolle Serie\" verschoben werden.</li><br>\n<li>Eine gruppierte Zeile wie <code>(Charakter A, Char A, Alternativname A)</code> bedeutet, dass Inhalte, die mit \"Charakter A\", \"Char A\" ODER \"Alternativname A\" übereinstimmen, ALLE in einen einzigen Ordner namens \"Charakter A Char A Alternativname A\" (nach Bereinigung) verschoben werden. Alle Begriffe in den Klammern werden zu Aliasen für diesen Ordner.</li></ul></li>\n<li><b>Intelligenter Fallback:</b> Wenn 'Getrennte Ordner nach Name/Titel' aktiv ist und ein Beitrag nicht mit einer spezifischen Eingabe von 'Nach Charakter(en) filtern' übereinstimmt, konsultiert der Downloader <code>Known.txt</code>, um einen passenden Hauptnamen für die Ordnererstellung zu finden.</li><br>\n<li><b>Benutzerfreundliche Verwaltung:</b> Fügen Sie einfache (nicht gruppierte) Namen über die UI-Liste unten hinzu. Für eine erweiterte Bearbeitung (wie das Erstellen/Ändern von gruppierten Aliasen) klicken Sie auf <b>'Known.txt öffnen'</b>, um die Datei in Ihrem Texteditor zu bearbeiten. Die App lädt sie bei der nächsten Verwendung oder beim Start neu.</li>\n</ul>\n</li>\n</ul>",
"tour_dialog_step7_title":"⑥ Häufige Fehler und Fehlerbehebung",
"tour_dialog_step7_content":"Manchmal können beim Herunterladen Probleme auftreten. Hier sind einige häufige:\n<ul>\n<li><b>Charakter-Eingabe-Tooltip:</b><br>\nGeben Sie Charakternamen ein, durch Kommas getrennt (z. B. <i>Tifa, Aerith</i>).<br>\nGruppieren Sie Aliase für einen gemeinsamen Ordnernamen: <i>(alias1, alias2, alias3)</i> wird zum Ordner 'alias1 alias2 alias3'.<br>\nAlle Namen in der Gruppe werden als Aliase für übereinstimmende Inhalte verwendet.<br><br>\nDie Schaltfläche 'Filter: [Typ]' neben dieser Eingabe schaltet um, wie dieser Filter angewendet wird:<br>\n- Filter: Dateien: Überprüft einzelne Dateinamen. Nur übereinstimmende Dateien werden heruntergeladen.<br>\n- Filter: Titel: Überprüft Beitragstitel. Alle Dateien aus einem übereinstimmenden Beitrag werden heruntergeladen.<br>\n- Filter: Beides: Überprüft zuerst den Beitragstitel. Wenn keine Übereinstimmung, werden die Dateinamen überprüft.<br>\n- Filter: Kommentare (Beta): Überprüft zuerst die Dateinamen. Wenn keine Übereinstimmung, werden die Kommentare des Beitrags überprüft.<br><br>\nDieser Filter beeinflusst auch die Ordnerbenennung, wenn 'Getrennte Ordner nach Name/Titel' aktiviert ist.</li><br>\n<li><b>502 Bad Gateway / 503 Service Unavailable / 504 Gateway Timeout:</b><br>\nDies deutet in der Regel auf vorübergehende serverseitige Probleme mit Kemono/Coomer hin. Die Seite ist möglicherweise überlastet, wegen Wartungsarbeiten ausgefallen oder hat Probleme.<br>\n<b>Lösung:</b> Warten Sie eine Weile (z. B. 30 Minuten bis einige Stunden) und versuchen Sie es später erneut. Überprüfen Sie die Seite direkt in Ihrem Browser.</li><br>\n<li><b>Verbindung verloren / Verbindung abgelehnt / Zeitüberschreitung (während des Dateidownloads):</b><br>\nDies kann aufgrund Ihrer Internetverbindung, Serverinstabilität oder wenn der Server die Verbindung für eine große Datei unterbricht, auftreten.<br>\n<b>Lösung:</b> Überprüfen Sie Ihre Internetverbindung. Versuchen Sie, die Anzahl der 'Threads' zu reduzieren, wenn sie hoch ist. Die App fordert Sie möglicherweise auf, einige fehlgeschlagene Dateien am Ende einer Sitzung erneut zu versuchen.</li><br>\n<li><b>IncompleteRead-Fehler:</b><br>\nDer Server hat weniger Daten gesendet als erwartet. Oft ein vorübergehender Netzwerkfehler oder ein Serverproblem.<br>\n<b>Lösung:</b> Die App markiert diese Dateien oft für einen erneuten Versuch am Ende der Download-Sitzung.</li><br>\n<li><b>403 Verboten / 401 Nicht autorisiert (seltener bei öffentlichen Beiträgen):</b><br>\nMöglicherweise haben Sie keine Berechtigung zum Zugriff auf den Inhalt. Bei einigen kostenpflichtigen oder privaten Inhalten kann die Verwendung der Option 'Cookie verwenden' mit gültigen Cookies aus Ihrer Browsersitzung helfen. Stellen Sie sicher, dass Ihre Cookies aktuell sind.</li><br>\n<li><b>404 Nicht gefunden:</b><br>\nDie Beitrags- oder Datei-URL ist falsch, oder der Inhalt wurde von der Seite entfernt. Überprüfen Sie die URL noch einmal.</li><br>\n<li><b>'Keine Beiträge gefunden' / 'Zielbeitrag nicht gefunden':</b><br>\nStellen Sie sicher, dass die URL korrekt ist und der Ersteller/Beitrag existiert. Wenn Sie Seitenbereiche verwenden, stellen Sie sicher, dass sie für den Ersteller gültig sind. Bei sehr neuen Beiträgen kann es eine leichte Verzögerung geben, bevor sie in der API erscheinen.</li><br>\n<li><b>Allgemeine Langsamkeit / App '(reagiert nicht)':</b><br>\nWie in Schritt 1 erwähnt, geben Sie der App bitte etwas Zeit, wenn sie nach dem Start zu hängen scheint, insbesondere bei großen Ersteller-Feeds oder vielen Threads. Sie verarbeitet wahrscheinlich Daten im Hintergrund. Das Reduzieren der Thread-Anzahl kann manchmal die Reaktionsfähigkeit verbessern, wenn dies häufig vorkommt.</li>\n</ul>",
"tour_dialog_step8_title":"⑦ Protokoll & Endgültige Steuerelemente",
"tour_dialog_step8_content":"Überwachung und Steuerelemente:\n<ul>\n<li><b>📜 Fortschrittsprotokoll / Protokoll der extrahierten Links:</b> Zeigt detaillierte Download-Nachrichten an. Wenn der Modus '🔗 Nur Links' aktiv ist, zeigt dieser Bereich die extrahierten Links an.</li><br>\n<li><b>Externe Links im Protokoll anzeigen:</b> Wenn aktiviert, erscheint unter dem Hauptprotokoll ein sekundäres Protokollfenster, um externe Links anzuzeigen, die in Beitragsbeschreibungen gefunden wurden. <i>(Dies ist deaktiviert, wenn der Modus '🔗 Nur Links' oder '📦 Nur Archive' aktiv ist).</i></li><br>\n<li><b>Protokollansicht-Umschalter (Schaltfläche 👁️ / 🙈):</b><br>\nDiese Schaltfläche (oben rechts im Protokollbereich) schaltet die Hauptprotokollansicht um:\n<ul><li><b>👁️ Fortschrittsprotokoll (Standard):</b> Zeigt alle Download-Aktivitäten, Fehler und Zusammenfassungen an.</li><br>\n<li><b>🙈 Protokoll verpasster Charaktere:</b> Zeigt eine Liste von Schlüsselbegriffen aus Beitragstiteln an, die aufgrund Ihrer 'Nach Charakter(en) filtern'-Einstellungen übersprungen wurden. Nützlich, um Inhalte zu identifizieren, die Sie möglicherweise unbeabsichtigt verpassen.</li></ul></li><br>\n<li><b>🔄 Zurücksetzen:</b> Löscht alle Eingabefelder, Protokolle und setzt temporäre Einstellungen auf ihre Standardwerte zurück. Kann nur verwendet werden, wenn kein Download aktiv ist.</li><br>\n<li><b>⬇️ Download starten / 🔗 Links extrahieren / ⏸️ Anhalten / ❌ Abbrechen:</b> Diese Schaltflächen steuern den Prozess. 'Abbrechen & UI zurücksetzen' stoppt den aktuellen Vorgang und führt einen weichen UI-Reset durch, wobei Ihre URL- und Verzeichniseingaben erhalten bleiben. 'Anhalten/Fortsetzen' ermöglicht das vorübergehende Anhalten und Fortsetzen.</li><br>\n<li>Wenn einige Dateien mit behebbaren Fehlern (wie 'IncompleteRead') fehlschlagen, werden Sie möglicherweise aufgefordert, sie am Ende einer Sitzung erneut zu versuchen.</li>\n</ul>\n<br>Sie sind bereit! Klicken Sie auf <b>'Fertigstellen'</b>, um die Tour zu schließen und den Downloader zu verwenden.",
"help_guide_dialog_title":"Kemono Downloader - Funktionshandbuch",
"help_guide_github_tooltip":"Besuchen Sie die GitHub-Seite des Projekts (öffnet sich im Browser)",
"help_guide_instagram_tooltip":"Besuchen Sie unsere Instagram-Seite (öffnet sich im Browser)",
"help_guide_discord_tooltip":"Besuchen Sie unsere Discord-Community (öffnet sich im Browser)",
"help_guide_step1_title":"① Einführung & Haupteingaben",
"help_guide_step1_content":"<html><head/><body>\n<p>Dieses Handbuch bietet einen Überblick über die Funktionen, Felder und Schaltflächen des Kemono Downloaders.</p>\n<h3>Haupteingabebereich (oben links)</h3>\n<ul>\n<li><b>🔗 Kemono Ersteller/Beitrags-URL:</b>\n<ul>\n<li>Geben Sie die vollständige Webadresse einer Erstellerseite (z. B. <i>https://kemono.su/patreon/user/12345</i>) oder eines bestimmten Beitrags (z. B. <i>.../post/98765</i>) ein.</li>\n<li>Unterstützt Kemono- (kemono.su, kemono.party) und Coomer-URLs (coomer.su, coomer.party).</li>\n</ul>\n</li>\n<li><b>Seitenbereich (Start bis Ende):</b>\n<ul>\n<li>Für Ersteller-URLs: Geben Sie einen Seitenbereich zum Abrufen an (z. B. Seiten 2 bis 5). Lassen Sie das Feld für alle Seiten leer.</li>\n<li>Deaktiviert für einzelne Beitrags-URLs oder wenn der <b>Manga/Comic-Modus</b> aktiv ist.</li>\n</ul>\n</li>\n<li><b>📁 Download-Speicherort:</b>\n<ul>\n<li>Klicken Sie auf <b>'Durchsuchen...'</b>, um einen Hauptordner auf Ihrem Computer auszuwählen, in dem alle heruntergeladenen Dateien gespeichert werden.</li>\n<li>Dieses Feld ist erforderlich, es sei denn, Sie verwenden den Modus <b>'🔗 Nur Links'</b>.</li>\n</ul>\n</li>\n<li><b>🎨 Erstellerauswahl-Schaltfläche (neben der URL-Eingabe):</b>\n<ul>\n<li>Klicken Sie auf das Palettensymbol (🎨), um das Dialogfeld 'Erstellerauswahl' zu öffnen.</li>\n<li>Dieses Dialogfeld lädt Ersteller aus Ihrer <code>creators.json</code>-Datei (die sich im Anwendungsverzeichnis befinden sollte).</li>\n<li><b>Innerhalb des Dialogfelds:</b>\n<ul>\n<li><b>Suchleiste:</b> Geben Sie Text ein, um die Liste der Ersteller nach Name oder Dienst zu filtern.</li>\n<li><b>Erstellerliste:</b> Zeigt Ersteller aus Ihrer <code>creators.json</code> an. Ersteller, die Sie als 'Favoriten' markiert haben (in den JSON-Daten), werden oben angezeigt.</li>\n<li><b>Kontrollkästchen:</b> Wählen Sie einen oder mehrere Ersteller aus, indem Sie das Kästchen neben ihrem Namen aktivieren.</li>\n<li><b>Schaltfläche 'Bereich' (z. B. 'Bereich: Charaktere'):</b> Diese Schaltfläche schaltet die Download-Organisation um, wenn Downloads aus diesem Popup gestartet werden:\n<ul><li><i>Bereich: Charaktere:</i> Downloads werden direkt in Ihrem Haupt-'Download-Speicherort' in nach Charakteren benannte Ordner organisiert. Arbeiten verschiedener Ersteller für denselben Charakter werden zusammengefasst.</li>\n<li><i>Bereich: Ersteller:</i> Downloads erstellen zuerst einen nach dem Ersteller benannten Ordner in Ihrem Haupt-'Download-Speicherort'. Dann werden in jedem Erstellerordner nach Charakteren benannte Unterordner erstellt.</li></ul>\n</li>\n<li><b>Schaltfläche 'Ausgewählte hinzufügen':</b> Wenn Sie hier klicken, werden die Namen aller aktivierten Ersteller übernommen und durch Kommas getrennt in das Haupteingabefeld '🔗 Kemono Ersteller/Beitrags-URL' eingefügt. Das Dialogfeld wird dann geschlossen.</li>\n</ul>\n</li>\n<li>Diese Funktion bietet eine schnelle Möglichkeit, das URL-Feld für mehrere Ersteller zu füllen, ohne jede URL manuell eingeben oder einfügen zu müssen.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step2_title":"② Downloads filtern",
"help_guide_step2_content":"<html><head/><body>\n<h3>Downloads filtern (linkes Panel)</h3>\n<ul>\n<li><b>🎯 Nach Charakter(en) filtern:</b>\n<ul>\n<li>Geben Sie Namen ein, durch Kommas getrennt (z. B. <code>Tifa, Aerith</code>).</li>\n<li><b>Gruppierte Aliase für freigegebenen Ordner (separate Known.txt-Einträge):</b> <code>(Vivi, Ulti, Uta)</code>.\n<ul><li>Inhalte, die mit \"Vivi\", \"Ulti\" ODER \"Uta\" übereinstimmen, werden in einen freigegebenen Ordner namens \"Vivi Ulti Uta\" verschoben (nach der Bereinigung).</li>\n<li>Wenn diese Namen neu sind, werden Sie aufgefordert, \"Vivi\", \"Ulti\" und \"Uta\" als <i>separate einzelne Einträge</i> zu <code>Known.txt</code> hinzuzufügen.</li>\n</ul>\n</li>\n<li><b>Gruppierte Aliase für freigegebenen Ordner (einzelner Known.txt-Eintrag):</b> <code>(Yuffie, Sonon)~</code> (beachten Sie die Tilde <code>~</code>).\n<ul><li>Inhalte, die mit \"Yuffie\" ODER \"Sonon\" übereinstimmen, werden in einen freigegebenen Ordner namens \"Yuffie Sonon\" verschoben.</li>\n<li>Wenn neu, werden Sie aufgefordert, \"Yuffie Sonon\" (mit den Aliasen Yuffie, Sonon) als <i>einzelnen Gruppeneintrag</i> zu <code>Known.txt</code> hinzuzufügen.</li>\n</ul>\n</li>\n<li>Dieser Filter beeinflusst die Ordnerbenennung, wenn 'Getrennte Ordner nach Name/Titel' aktiviert ist.</li>\n</ul>\n</li>\n<li><b>Filter: Schaltfläche [Typ] (Charakterfilterbereich):</b> Schaltet um, wie 'Nach Charakter(en) filtern' angewendet wird:\n<ul>\n<li><code>Filter: Dateien</code>: Überprüft einzelne Dateinamen. Ein Beitrag wird beibehalten, wenn eine Datei übereinstimmt; nur übereinstimmende Dateien werden heruntergeladen. Die Ordnerbenennung verwendet den Charakter aus dem übereinstimmenden Dateinamen.</li>\n<li><code>Filter: Titel</code>: Überprüft Beitragstitel. Alle Dateien aus einem übereinstimmenden Beitrag werden heruntergeladen. Die Ordnerbenennung verwendet den Charakter aus dem übereinstimmenden Beitragstitel.</li>\n<li><code>Filter: Beides</code>: Überprüft zuerst den Beitragstitel. Wenn er übereinstimmt, werden alle Dateien heruntergeladen. Wenn nicht, werden die Dateinamen überprüft und nur übereinstimmende Dateien heruntergeladen. Die Ordnerbenennung priorisiert die Titelübereinstimmung, dann die Dateiübereinstimmung.</li>\n<li><code>Filter: Kommentare (Beta)</code>: Überprüft zuerst die Dateinamen. Wenn eine Datei übereinstimmt, werden alle Dateien aus dem Beitrag heruntergeladen. Wenn keine Dateiübereinstimmung vorliegt, werden die Kommentare des Beitrags überprüft. Wenn ein Kommentar übereinstimmt, werden alle Dateien heruntergeladen. (Verwendet mehr API-Anfragen). Die Ordnerbenennung priorisiert die Dateiübereinstimmung, dann die Kommentarübereinstimmung.</li>\n</ul>\n</li>\n<li><b>🗄️ Benutzerdefinierter Ordnername (nur einzelner Beitrag):</b>\n<ul>\n<li>Nur sichtbar und verwendbar, wenn eine einzelne spezifische Beitrags-URL heruntergeladen wird UND 'Getrennte Ordner nach Name/Titel' aktiviert ist.</li>\n<li>Ermöglicht die Angabe eines benutzerdefinierten Namens für den Download-Ordner dieses einzelnen Beitrags.</li>\n</ul>\n</li>\n<li><b>🚫 Mit Wörtern überspringen:</b>\n<ul><li>Geben Sie Wörter, durch Kommas getrennt, ein (z. B. <code>WIP, sketch, preview</code>), um bestimmte Inhalte zu überspringen.</li></ul>\n</li>\n<li><b>Bereich: Schaltfläche [Typ] (Bereich der zu überspringenden Wörter):</b> Schaltet um, wie 'Mit Wörtern überspringen' angewendet wird:\n<ul>\n<li><code>Bereich: Dateien</code>: Überspringt einzelne Dateien, wenn ihre Namen eines dieser Wörter enthalten.</li>\n<li><code>Bereich: Beiträge</code>: Überspringt ganze Beiträge, wenn ihre Titel eines dieser Wörter enthalten.</li>\n<li><code>Bereich: Beides</code>: Wendet beides an (zuerst Beitragstitel, dann einzelne Dateien).</li>\n</ul>\n</li>\n<li><b>✂️ Wörter aus dem Namen entfernen:</b>\n<ul><li>Geben Sie Wörter, durch Kommas getrennt, ein (z. B. <code>patreon, [HD]</code>), die aus den heruntergeladenen Dateinamen entfernt werden sollen (Groß-/Kleinschreibung wird nicht beachtet).</li></ul>\n</li>\n<li><b>Dateien filtern (Radioschaltflächen):</b> Wählen Sie aus, was heruntergeladen werden soll:\n<ul>\n<li><code>Alles</code>: Lädt alle gefundenen Dateitypen herunter.</li>\n<li><code>Bilder/GIFs</code>: Nur gängige Bildformate (JPG, PNG, GIF, WEBP usw.) und GIFs.</li>\n<li><code>Videos</code>: Nur gängige Videoformate (MP4, MKV, WEBM, MOV usw.).</li>\n<li><code>📦 Nur Archive</code>: Lädt ausschließlich <b>.zip</b>- und <b>.rar</b>-Dateien herunter. Wenn diese Option ausgewählt ist, werden die Kontrollkästchen 'zip überspringen' und '.rar überspringen' automatisch deaktiviert und abgewählt. 'Externe Links anzeigen' wird ebenfalls deaktiviert.</li>\n<li><code>🎧 Nur Audio</code>: Lädt nur gängige Audioformate (MP3, WAV, FLAC, M4A, OGG usw.) herunter. Andere dateispezifische Optionen verhalten sich wie im Modus 'Bilder' oder 'Videos'.</li>\n<li><code>🔗 Nur Links</code>: Extrahiert und zeigt externe Links aus Beitragsbeschreibungen an, anstatt Dateien herunterzuladen. Download-bezogene Optionen und 'Externe Links anzeigen' werden deaktiviert. Die Haupt-Download-Schaltfläche ändert sich in '🔗 Links extrahieren'.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step3_title":"③ Download-Optionen & Einstellungen",
"help_guide_step3_content":"<html><head/><body>\n<h3>Download-Optionen & Einstellungen (linkes Panel)</h3>\n<ul>\n<li><b>.zip überspringen / .rar überspringen:</b> Kontrollkästchen, um das Herunterladen dieser Archivdateitypen zu vermeiden. (Deaktiviert und ignoriert, wenn der Filtermodus '📦 Nur Archive' ausgewählt ist).</li>\n<li><b>Nur Miniaturansichten herunterladen:</b> Lädt kleine Vorschaubilder anstelle von Dateien in voller Größe herunter (falls verfügbar).</li>\n<li><b>Große Bilder komprimieren (in WebP):</b> Wenn die 'Pillow'-Bibliothek (PIL) installiert ist, werden Bilder, die größer als 1,5 MB sind, in das WebP-Format konvertiert, wenn die WebP-Version deutlich kleiner ist.</li>\n<li><b>⚙️ Erweiterte Einstellungen:</b>\n<ul>\n<li><b>Getrennte Ordner nach Name/Titel:</b> Erstellt Unterordner basierend auf der Eingabe 'Nach Charakter(en) filtern' oder den Beitragstiteln. Kann die Liste <b>Known.txt</b> als Fallback für Ordnernamen verwenden.</li></ul></li></ul></body></html>",
"help_guide_step4_title":"④ Erweiterte Einstellungen (Teil 1)",
"help_guide_step4_content":"<html><head/><body><h3>⚙️ Erweiterte Einstellungen (Fortsetzung)</h3><ul><ul>\n<li><b>Unterordner pro Beitrag:</b> Wenn 'Getrennte Ordner' aktiviert ist, wird für <i>jeden einzelnen Beitrag</i> ein zusätzlicher Unterordner im Hauptordner für den Charakter/Titel erstellt.</li>\n<li><b>Cookie verwenden:</b> Aktivieren Sie dieses Kontrollkästchen, um Cookies für Anfragen zu verwenden.\n<ul>\n<li><b>Textfeld:</b> Geben Sie eine Cookie-Zeichenfolge direkt ein (z. B. <code>name1=value1; name2=value2</code>).</li>\n<li><b>Durchsuchen...:</b> Wählen Sie eine <code>cookies.txt</code>-Datei (Netscape-Format) aus. Der Pfad wird im Textfeld angezeigt.</li>\n<li><b>Vorrang:</b> Das Textfeld (wenn ausgefüllt) hat Vorrang vor einer durchsuchten Datei. Wenn 'Cookie verwenden' aktiviert ist, aber beide leer sind, wird versucht, <code>cookies.txt</code> aus dem Anwendungsverzeichnis zu laden.</li>\n</ul>\n</li>\n<li><b>Multithreading verwenden & Threads-Eingabe:</b>\n<ul>\n<li>Aktiviert schnellere Operationen. Die Zahl in der Eingabe 'Threads' bedeutet:\n<ul>\n<li>Für <b>Ersteller-Feeds:</b> Anzahl der gleichzeitig zu verarbeitenden Beiträge. Dateien innerhalb jedes Beitrags werden von seinem Worker nacheinander heruntergeladen (es sei denn, die Manga-Benennung 'Datumsbasiert' ist aktiviert, was 1 Beitrags-Worker erzwingt).</li>\n<li>Für <b>einzelne Beitrags-URLs:</b> Anzahl der gleichzeitig von diesem einzelnen Beitrag herunterzuladenden Dateien.</li>\n</ul>\n</li>\n<li>Wenn nicht aktiviert, wird 1 Thread verwendet. Hohe Thread-Zahlen (z. B. >40) können einen Hinweis anzeigen.</li>\n</ul>\n</li></ul></ul></body></html>",
"help_guide_step5_title":"⑤ Erweiterte Einstellungen (Teil 2) & Aktionen",
"help_guide_step5_content":"<html><head/><body><h3>⚙️ Erweiterte Einstellungen (Fortsetzung)</h3><ul><ul>\n<li><b>Externe Links im Protokoll anzeigen:</b> Wenn aktiviert, erscheint unter dem Hauptprotokoll ein sekundäres Protokollfenster, um externe Links anzuzeigen, die in Beitragsbeschreibungen gefunden wurden. (Deaktiviert, wenn der Modus '🔗 Nur Links' oder '📦 Nur Archive' aktiv ist).</li>\n<li><b>📖 Manga/Comic-Modus (nur Ersteller-URL):</b> Speziell für sequentielle Inhalte.\n<ul>\n<li>Lädt Beiträge vom <b>ältesten zum neuesten</b> herunter.</li>\n<li>Die Eingabe 'Seitenbereich' ist deaktiviert, da alle Beiträge abgerufen werden.</li>\n<li>Eine <b>Schaltfläche zum Umschalten des Dateinamenstils</b> (z. B. 'Name: Beitragstitel') erscheint oben rechts im Protokollbereich, wenn dieser Modus für einen Ersteller-Feed aktiv ist. Klicken Sie darauf, um zwischen den Benennungsstilen zu wechseln:\n<ul>\n<li><code>Name: Beitragstitel (Standard)</code>: Die erste Datei in einem Beitrag wird nach dem bereinigten Titel des Beitrags benannt (z. B. 'Mein Kapitel 1.jpg'). Nachfolgende Dateien im *gleichen Beitrag* versuchen, ihre ursprünglichen Dateinamen beizubehalten (z. B. 'seite_02.png', 'bonus_art.jpg'). Wenn der Beitrag nur eine Datei hat, wird sie nach dem Beitragstitel benannt. Dies wird im Allgemeinen für die meisten Mangas/Comics empfohlen.</li>\n<li><code>Name: Originaldatei</code>: Alle Dateien versuchen, ihre ursprünglichen Dateinamen beizubehalten.</li>\n<li><code>Name: Originaldatei</code>: Alle Dateien versuchen, ihre ursprünglichen Dateinamen beizubehalten. Wenn dieser Stil aktiv ist, erscheint neben dieser Stil-Schaltfläche ein Eingabefeld für ein <b>optionales Dateinamenpräfix</b> (z. B. 'MeineSerie_'). Beispiel: 'MeineSerie_Originaldatei.jpg'.</li>\n<li><code>Name: Titel+G.Nr. (Beitragstitel + Globale Nummerierung)</code>: Alle Dateien in allen Beiträgen der aktuellen Download-Sitzung werden sequentiell unter Verwendung des bereinigten Beitragstitels als Präfix benannt, gefolgt von einem globalen Zähler. Beispiel: Beitrag 'Kapitel 1' (2 Dateien) -> 'Kapitel 1 001.jpg', 'Kapitel 1 002.png'. Nächster Beitrag 'Kapitel 2' (1 Datei) -> 'Kapitel 2 003.jpg'. Multithreading für die Beitragsverarbeitung wird für diesen Stil automatisch deaktiviert.</li>\n<li><code>Name: Datumsbasiert</code>: Dateien werden sequentiell (001.ext, 002.ext, ...) basierend auf der Veröffentlichungsreihenfolge benannt. Wenn dieser Stil aktiv ist, erscheint neben dieser Stil-Schaltfläche ein Eingabefeld für ein <b>optionales Dateinamenpräfix</b> (z. B. 'MeineSerie_'). Beispiel: 'MeineSerie_001.jpg'. Multithreading für die Beitragsverarbeitung wird für diesen Stil automatisch deaktiviert.</li>\n</ul>\n</li>\n<li>Um mit den Stilen 'Name: Beitragstitel', 'Name: Titel+G.Nr.' oder 'Name: Datumsbasiert' die besten Ergebnisse zu erzielen, verwenden Sie das Feld 'Nach Charakter(en) filtern' mit dem Manga-/Serientitel für die Ordnerorganisation.</li>\n</ul>\n</li>\n</ul></li></ul>\n<h3>Hauptaktionsschaltflächen (linkes Panel)</h3>\n<ul>\n<li><b>⬇️ Download starten / 🔗 Links extrahieren:</b> Der Text und die Funktion dieser Schaltfläche ändern sich je nach Auswahl der Radioschaltfläche 'Dateien filtern'. Sie startet den Hauptvorgang.</li>\n<li><b>⏸️ Download anhalten / ▶️ Download fortsetzen:</b> Ermöglicht das vorübergehende Anhalten des aktuellen Download-/Extraktionsprozesses und die spätere Fortsetzung. Einige UI-Einstellungen können während der Pause geändert werden.</li>\n<li><b>❌ Abbrechen & UI zurücksetzen:</b> Stoppt den aktuellen Vorgang und führt einen weichen UI-Reset durch. Ihre URL- und Download-Verzeichniseingaben bleiben erhalten, aber andere Einstellungen und Protokolle werden gelöscht.</li>\n</ul></body></html>",
"help_guide_step6_title":"⑥ Liste bekannter Shows/Charaktere",
"help_guide_step6_content":"<html><head/><body>\n<h3>Verwaltung der Liste bekannter Shows/Charaktere (unten links)</h3>\n<p>Dieser Abschnitt hilft bei der Verwaltung der <code>Known.txt</code>-Datei, die für die intelligente Ordnerorganisation verwendet wird, wenn 'Getrennte Ordner nach Name/Titel' aktiviert ist, insbesondere als Fallback, wenn ein Beitrag nicht mit Ihrer aktiven Eingabe 'Nach Charakter(en) filtern' übereinstimmt.</p>\n<ul>\n<li><b>Known.txt öffnen:</b> Öffnet die <code>Known.txt</code>-Datei (im Anwendungsverzeichnis) in Ihrem Standard-Texteditor für eine erweiterte Bearbeitung (wie das Erstellen komplexer gruppierter Aliase).</li>\n<li><b>Charaktere suchen...:</b> Filtert die unten angezeigte Liste bekannter Namen.</li>\n<li><b>Listen-Widget:</b> Zeigt die Hauptnamen aus Ihrer <code>Known.txt</code> an. Wählen Sie hier Einträge aus, um sie zu löschen.</li>\n<li><b>Neuen Show-/Charakternamen hinzufügen (Eingabefeld):</b> Geben Sie einen Namen oder eine Gruppe zum Hinzufügen ein.\n<ul>\n<li><b>Einfacher Name:</b> z. B. <code>Meine tolle Serie</code>. Fügt als einzelnen Eintrag hinzu.</li>\n<li><b>Gruppe für separate Known.txt-Einträge:</b> z. B. <code>(Vivi, Ulti, Uta)</code>. Fügt \"Vivi\", \"Ulti\" und \"Uta\" als drei separate einzelne Einträge zu <code>Known.txt</code> hinzu.</li>\n<li><b>Gruppe für freigegebenen Ordner & einzelnen Known.txt-Eintrag (Tilde <code>~</code>):</b> z. B. <code>(Charakter A, Char A)~</code>. Fügt einen Eintrag zu <code>Known.txt</code> mit dem Namen \"Charakter A Char A\" hinzu. \"Charakter A\" und \"Char A\" werden zu Aliasen für diesen einzelnen Ordner/Eintrag.</li>\n</ul>\n</li>\n<li><b>➕ Hinzufügen-Schaltfläche:</b> Fügt den Namen/die Gruppe aus dem obigen Eingabefeld zur Liste und zu <code>Known.txt</code> hinzu.</li>\n<li><b>⤵️ Zum Filter hinzufügen-Schaltfläche:</b>\n<ul>\n<li>Befindet sich neben der '➕ Hinzufügen'-Schaltfläche für die Liste 'Bekannte Shows/Charaktere'.</li>\n<li>Durch Klicken auf diese Schaltfläche wird ein Popup-Fenster geöffnet, in dem alle Namen aus Ihrer <code>Known.txt</code>-Datei mit jeweils einem Kontrollkästchen angezeigt werden.</li>\n<li>Das Popup enthält eine Suchleiste zum schnellen Filtern der Namensliste.</li>\n<li>Sie können einen oder mehrere Namen über die Kontrollkästchen auswählen.</li>\n<li>Klicken Sie auf 'Ausgewählte hinzufügen', um die ausgewählten Namen in das Eingabefeld 'Nach Charakter(en) filtern' im Hauptfenster einzufügen.</li>\n<li>Wenn ein ausgewählter Name aus <code>Known.txt</code> ursprünglich eine Gruppe war (z. B. in Known.txt als <code>(Boa, Hancock)</code> definiert), wird er als <code>(Boa, Hancock)~</code> zum Filterfeld hinzugefügt. Einfache Namen werden unverändert hinzugefügt.</li>\n<li>Zur Vereinfachung sind im Popup die Schaltflächen 'Alle auswählen' und 'Alle abwählen' verfügbar.</li>\n<li>Klicken Sie auf 'Abbrechen', um das Popup ohne Änderungen zu schließen.</li>\n</ul>\n</li>\n<li><b>🗑️ Ausgewählte löschen-Schaltfläche:</b> Löscht die ausgewählten Namen aus der Liste und aus <code>Known.txt</code>.</li>\n<li><b>❓ Schaltfläche (genau diese!):</b> Zeigt diese umfassende Hilfeanleitung an.</li>\n</ul></body></html>",
"help_guide_step7_title":"⑦ Protokollbereich & Steuerelemente",
"help_guide_step7_content":"<html><head/><body>\n<h3>Protokollbereich & Steuerelemente (rechtes Panel)</h3>\n<ul>\n<li><b>📜 Fortschrittsprotokoll / Protokoll der extrahierten Links (Beschriftung):</b> Titel für den Hauptprotokollbereich; ändert sich, wenn der Modus '🔗 Nur Links' aktiv ist.</li>\n<li><b>Links suchen... / 🔍 Schaltfläche (Link-Suche):</b>\n<ul><li>Nur sichtbar, wenn der Modus '🔗 Nur Links' aktiv ist. Ermöglicht das Echtzeit-Filtern der im Hauptprotokoll angezeigten extrahierten Links nach Text, URL oder Plattform.</li></ul>\n</li>\n<li><b>Name: Schaltfläche [Stil] (Manga-Dateinamenstil):</b>\n<ul><li>Nur sichtbar, wenn der <b>Manga/Comic-Modus</b> für einen Ersteller-Feed aktiv ist und nicht im Modus 'Nur Links' oder 'Nur Archive'.</li>\n<li>Schaltet zwischen den Dateinamenstilen um: <code>Beitragstitel</code>, <code>Originaldatei</code>, <code>Datumsbasiert</code>. (Siehe Abschnitt Manga/Comic-Modus für Details).</li>\n<li>Wenn der Stil 'Originaldatei' oder 'Datumsbasiert' aktiv ist, erscheint neben dieser Schaltfläche ein Eingabefeld für ein <b>optionales Dateinamenpräfix</b>.</li>\n</ul>\n</li>\n<li><b>Mehrteilig: Schaltfläche [EIN/AUS]:</b>\n<ul><li>Schaltet mehrsegmentige Downloads für einzelne große Dateien um.\n<ul><li><b>EIN:</b> Kann das Herunterladen großer Dateien (z. B. Videos) beschleunigen, kann aber die Benutzeroberfläche bei vielen kleinen Dateien ruckeln lassen oder zu Protokoll-Spam führen. Beim Aktivieren wird ein Hinweis angezeigt. Wenn ein mehrteiliger Download fehlschlägt, wird er als Einzelstream wiederholt.</li>\n<li><b>AUS (Standard):</b> Dateien werden in einem einzigen Stream heruntergeladen.</li>\n</ul>\n<li>Deaktiviert, wenn der Modus '🔗 Nur Links' oder '📦 Nur Archive' aktiv ist.</li>\n</ul>\n</li>\n<li><b>👁️ / 🙈 Schaltfläche (Protokollansicht-Umschalter):</b> Schaltet die Hauptprotokollansicht um:\n<ul>\n<li><b>👁️ Fortschrittsprotokoll (Standard):</b> Zeigt alle Download-Aktivitäten, Fehler und Zusammenfassungen an.</li>\n<li><b>🙈 Protokoll verpasster Charaktere:</b> Zeigt eine Liste von Schlüsselbegriffen aus Beitrags-/Inhaltstiteln an, die aufgrund Ihrer 'Nach Charakter(en) filtern'-Einstellungen übersprungen wurden. Nützlich, um Inhalte zu identifizieren, die Sie möglicherweise unbeabsichtigt verpassen.</li>\n</ul>\n</li>\n<li><b>🔄 Zurücksetzen-Schaltfläche:</b> Löscht alle Eingabefelder, Protokolle und setzt temporäre Einstellungen auf ihre Standardwerte zurück. Kann nur verwendet werden, wenn kein Download aktiv ist.</li>\n<li><b>Hauptprotokollausgabe (Textbereich):</b> Zeigt detaillierte Fortschrittsmeldungen, Fehler und Zusammenfassungen an. Wenn der Modus '🔗 Nur Links' aktiv ist, zeigt dieser Bereich die extrahierten Links an.</li>\n<li><b>Protokollausgabe verpasster Charaktere (Textbereich):</b> (Sichtbar über den Umschalter 👁️ / 🙈) Zeigt Beiträge/Dateien an, die aufgrund von Charakterfiltern übersprungen wurden.</li>\n<li><b>Externe Protokollausgabe (Textbereich):</b> Erscheint unter dem Hauptprotokoll, wenn 'Externe Links im Protokoll anzeigen' aktiviert ist. Zeigt externe Links an, die in Beitragsbeschreibungen gefunden wurden.</li>\n<li><b>Links exportieren-Schaltfläche:</b>\n<ul><li>Nur sichtbar und aktiviert, wenn der Modus '🔗 Nur Links' aktiv ist und Links extrahiert wurden.</li>\n<li>Ermöglicht das Speichern aller extrahierten Links in einer <code>.txt</code>-Datei.</li>\n</ul>\n</li>\n<li><b>Fortschritt: Beschriftung [Status]:</b> Zeigt den Gesamtfortschritt des Download- oder Link-Extraktionsprozesses an (z. B. verarbeitete Beiträge).</li>\n<li><b>Dateifortschrittsbeschriftung:</b> Zeigt den Fortschritt einzelner Dateidownloads an, einschließlich Geschwindigkeit und Größe, oder den Status des mehrteiligen Downloads.</li>\n</ul></body></html>",
"help_guide_step8_title":"⑧ Favoritenmodus & Zukünftige Funktionen",
"help_guide_step8_content":"<html><head/><body>\n<h3>Favoritenmodus (Herunterladen aus Ihren Kemono.su-Favoriten)</h3>\n<p>Dieser Modus ermöglicht das direkte Herunterladen von Inhalten von Künstlern, die Sie auf Kemono.su als Favoriten markiert haben.</p>\n<ul>\n<li><b>⭐ Aktivierung:</b>\n<ul>\n<li>Aktivieren Sie das Kontrollkästchen <b>'⭐ Favoritenmodus'</b> neben der Radioschaltfläche '🔗 Nur Links'.</li>\n</ul>\n</li>\n<li><b>UI-Änderungen im Favoritenmodus:</b>\n<ul>\n<li>Der Eingabebereich '🔗 Kemono Ersteller/Beitrags-URL' wird durch eine Meldung ersetzt, die anzeigt, dass der Favoritenmodus aktiv ist.</li>\n<li>Die Standard-Schaltflächen 'Download starten', 'Anhalten', 'Abbrechen' werden ersetzt durch:\n<ul>\n<li><b>'🖼️ Lieblingskünstler'</b>-Schaltfläche</li>\n<li><b>'📄 Lieblingsbeiträge'</b>-Schaltfläche</li>\n</ul>\n</li>\n<li>Die Option '🍪 Cookie verwenden' wird automatisch aktiviert und gesperrt, da Cookies zum Abrufen Ihrer Favoriten erforderlich sind.</li>\n</ul>\n</li>\n<li><b>🖼️ Lieblingskünstler-Schaltfläche:</b>\n<ul>\n<li>Durch Klicken hier wird ein Dialogfeld geöffnet, in dem alle Künstler aufgelistet sind, die Sie auf Kemono.su als Favoriten markiert haben.</li>\n<li>Sie können einen oder mehrere Künstler aus dieser Liste auswählen, um deren Inhalte herunterzuladen.</li>\n</ul>\n</li>\n<li><b>📄 Lieblingsbeiträge-Schaltfläche (Zukünftige Funktion):</b>\n<ul>\n<li>Das Herunterladen bestimmter favorisierter <i>Beiträge</i> (insbesondere in einer sequentiellen Reihenfolge wie bei Mangas, wenn sie Teil einer Serie sind) ist eine Funktion, die sich derzeit in der Entwicklung befindet.</li>\n<li>Die beste Vorgehensweise für favorisierte Beiträge, insbesondere für sequentielles Lesen wie bei Mangas, wird noch untersucht.</li>\n<li>Wenn Sie spezielle Ideen oder Anwendungsfälle haben, wie Sie favorisierte Beiträge herunterladen und organisieren möchten (z. B. 'Manga-Stil' aus Favoriten), erwägen Sie bitte, ein Issue zu eröffnen oder an der Diskussion auf der GitHub-Seite des Projekts teilzunehmen. Ihr Beitrag ist wertvoll!</li>\n</ul>\n</li>\n<li><b>Favoriten-Download-Bereich (Schaltfläche):</b>\n<ul>\n<li>Diese Schaltfläche (neben 'Lieblingsbeiträge') steuert, wohin Inhalte von ausgewählten Lieblingskünstlern heruntergeladen werden:\n<ul>\n<li><b><i>Bereich: Ausgewählter Ort:</i></b> Alle ausgewählten Künstler werden in den in der Benutzeroberfläche festgelegten Haupt-'Download-Speicherort' heruntergeladen. Filter gelten global für alle Inhalte.</li>\n<li><b><i>Bereich: Künstlerordner:</i></b> Für jeden ausgewählten Künstler wird automatisch ein Unterordner (benannt nach dem Künstler) in Ihrem Haupt-'Download-Speicherort' erstellt. Inhalte für diesen Künstler werden in ihren spezifischen Unterordner verschoben. Filter werden innerhalb des dedizierten Ordners jedes Künstlers angewendet.</li>\n</ul>\n</li>\n</ul>\n</li>\n<li><b>Filter im Favoritenmodus:</b>\n<ul>\n<li>Die in der Benutzeroberfläche festgelegten Optionen '🎯 Nach Charakter(en) filtern', '🚫 Mit Wörtern überspringen' und 'Dateien filtern' gelten weiterhin für die von Ihren ausgewählten Lieblingskünstlern heruntergeladenen Inhalte.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step9_title":"⑨ Schlüsseldateien & Tour",
"help_guide_step9_content":"<html><head/><body>\n<h3>Von der Anwendung verwendete Schlüsseldateien</h3>\n<ul>\n<li><b><code>Known.txt</code>:</b>\n<ul>\n<li>Befindet sich im Anwendungsverzeichnis (wo sich die <code>.exe</code> oder <code>main.py</code> befindet).</li>\n<li>Speichert Ihre Liste bekannter Shows, Charaktere oder Serientitel für die automatische Ordnerorganisation, wenn 'Getrennte Ordner nach Name/Titel' aktiviert ist.</li>\n<li><b>Format:</b>\n<ul>\n<li>Jede Zeile ist ein Eintrag.</li>\n<li><b>Einfacher Name:</b> z. B. <code>Meine tolle Serie</code>. Inhalte, die damit übereinstimmen, werden in einen Ordner namens \"Meine tolle Serie\" verschoben.</li>\n<li><b>Gruppierte Aliase:</b> z. B. <code>(Charakter A, Char A, Alternativname A)</code>. Inhalte, die mit \"Charakter A\", \"Char A\" ODER \"Alternativname A\" übereinstimmen, werden ALLE in einen einzigen Ordner namens \"Charakter A Char A Alternativname A\" (nach Bereinigung) verschoben. Alle Begriffe in den Klammern werden zu Aliasen für diesen Ordner.</li>\n</ul>\n</li>\n<li><b>Verwendung:</b> Dient als Fallback für die Ordnerbenennung, wenn ein Beitrag nicht mit Ihrer aktiven Eingabe 'Nach Charakter(en) filtern' übereinstimmt. Sie können einfache Einträge über die Benutzeroberfläche verwalten oder die Datei direkt für komplexe Aliase bearbeiten. Die App lädt sie beim Start oder bei der nächsten Verwendung neu.</li>\n</ul>\n</li>\n<li><b><code>cookies.txt</code> (Optional):</b>\n<ul>\n<li>Wenn Sie die Funktion 'Cookie verwenden' verwenden und keine direkte Cookie-Zeichenfolge angeben oder zu einer bestimmten Datei navigieren, sucht die Anwendung in ihrem Verzeichnis nach einer Datei namens <code>cookies.txt</code>.</li>\n<li><b>Format:</b> Muss im Netscape-Cookie-Dateiformat vorliegen.</li>\n<li><b>Verwendung:</b> Ermöglicht dem Downloader, die Anmeldesitzung Ihres Browsers zu verwenden, um auf Inhalte zuzugreifen, die möglicherweise eine Anmeldung auf Kemono/Coomer erfordern.</li>\n</ul>\n</li>\n</ul>\n<h3>Tour für Erstbenutzer</h3>\n<ul>\n<li>Beim ersten Start (oder bei einem Reset) erscheint ein Willkommens-Tour-Dialogfeld, das Sie durch die Hauptfunktionen führt. Sie können es überspringen oder 'Diese Tour nie wieder anzeigen' auswählen.</li>\n</ul>\n<p><em>Viele UI-Elemente haben auch Tooltips, die erscheinen, wenn Sie mit der Maus darüber fahren, und schnelle Hinweise geben.</em></p>\n</body></html>"
})

translations ["pt"]={}
translations ["pt"].update ({
"settings_dialog_title":"Configurações",
"language_label":"Idioma:",
"lang_english":"Inglês (English)",
"lang_japanese":"Japonês (日本語)",
"theme_toggle_light":"Mudar para o modo claro",
"theme_toggle_dark":"Mudar para o modo escuro",
"theme_tooltip_light":"Mudar a aparência da aplicação para claro.",
"theme_tooltip_dark":"Mudar a aparência da aplicación para escuro.",
"ok_button":"OK",
"appearance_group_title":"Aparência",
"language_group_title":"Configurações de idioma",
"creator_post_url_label":"🔗 URL do Criador/Post do Kemono:",
"download_location_label":"📁 Local de Download:",
"filter_by_character_label":"🎯 Filtrar por Personagem(ns) (separados por vírgula):",
"skip_with_words_label":"🚫 Ignorar com Palavras (separadas por vírgula):",
"remove_words_from_name_label":"✂️ Remover Palavras do nome:",
"filter_all_radio":"Todos",
"filter_images_radio":"Imagens/GIFs",
"filter_videos_radio":"Vídeos",
"filter_archives_radio":"📦 Apenas Arquivos",
"filter_links_radio":"🔗 Apenas Links",
"filter_audio_radio":"🎧 Apenas Áudio",
"favorite_mode_checkbox_label":"⭐ Modo Favoritos",
"browse_button_text":"Procurar...",
"char_filter_scope_files_text":"Filtro: Arquivos",
"char_filter_scope_files_tooltip":"Escopo atual: Arquivos\n\nFiltra arquivos individuais por nome. Uma publicação é mantida se algum arquivo corresponder.\nSomente os arquivos correspondentes dessa publicação são baixados.\nExemplo: Filtro 'Tifa'. O arquivo 'Tifa_artwork.jpg' corresponde e é baixado.\nNomenclatura da pasta: Usa o personagem do nome do arquivo correspondente.\n\nClique para alternar para: Ambos",
"char_filter_scope_title_text":"Filtro: Título",
"char_filter_scope_title_tooltip":"Escopo atual: Título\n\nFiltra publicações inteiras por seu título. Todos os arquivos de uma publicação correspondente são baixados.\nExemplo: Filtro 'Aerith'. A publicação intitulada 'Jardim de Aerith' corresponde; todos os seus arquivos são baixados.\nNomenclatura da pasta: Usa o personagem do título da publicação correspondente.\n\nClique para alternar para: Arquivos",
"char_filter_scope_both_text":"Filtro: Ambos",
"char_filter_scope_both_tooltip":"Escopo atual: Ambos (Título e depois Arquivos)\n\n1. Verifica o título da publicação: Se corresponder, todos os arquivos da publicação são baixados.\n2. Se o título não corresponder, verifica os nomes dos arquivos: Se algum arquivo corresponder, apenas esse arquivo é baixado.\nExemplo: Filtro 'Cloud'.\n - Publicação 'Cloud Strife' (correspondência de título) -> todos os arquivos são baixados.\n - Publicação 'Perseguição de Moto' com 'Cloud_fenrir.jpg' (correspondência de arquivo) -> apenas 'Cloud_fenrir.jpg' é baixado.\nNomenclatura da pasta: Prioriza a correspondência de título, depois a correspondência de arquivo.\n\nClique para alternar para: Comentários",
"char_filter_scope_comments_text":"Filtro: Comentários (Beta)",
"char_filter_scope_comments_tooltip":"Escopo atual: Comentários (Beta - Arquivos primeiro, depois Comentários como fallback)\n\n1. Verifica os nomes dos arquivos: Se algum arquivo na publicação corresponder ao filtro, a publicação inteira é baixada. Os comentários NÃO são verificados para este termo de filtro.\n2. Se nenhum arquivo corresponder, ENTÃO verifica os comentários da publicação: Se um comentário corresponder, a publicação inteira é baixada.\nExemplo: Filtro 'Barret'.\n - Publicação A: Arquivos 'Barret_gunarm.jpg', 'other.png'. O arquivo 'Barret_gunarm.jpg' corresponde. Todos os arquivos da Publicação A são baixados. Os comentários não são verificados para 'Barret'.\n - Publicação B: Arquivos 'dyne.jpg', 'weapon.gif'. Comentários: '...um desenho de Barret Wallace...'. Nenhuma correspondência de arquivo para 'Barret'. O comentário corresponde. Todos os arquivos da Publicação B são baixados.\nNomenclatura da pasta: Prioriza o personagem da correspondência de arquivo, depois da correspondência de comentário.\n\nClique para alternar para: Título",
"char_filter_scope_unknown_text":"Filtro: Desconhecido",
"char_filter_scope_unknown_tooltip":"Escopo atual: Desconhecido\n\nO escopo do filtro de personagem está em um estado desconhecido. Por favor, alterne ou reinicie.\n\nClique para alternar para: Título",
"skip_words_input_tooltip":"Digite palavras, separadas por vírgula, para pular o download de determinados conteúdos (ex: WIP, rascunho, prévia).\n\nO botão 'Escopo: [Tipo]' ao lado desta entrada alterna como este filtro se aplica:\n- Escopo: Arquivos: Pula arquivos individuais se seus nomes contiverem alguma dessas palavras.\n- Escopo: Publicações: Pula publicações inteiras se seus títulos contiverem alguma dessas palavras.\n- Escopo: Ambos: Aplica ambos (primeiro o título da publicação, depois os arquivos individuais se o título da publicação estiver OK).",
"remove_words_input_tooltip":"Digite palavras, separadas por vírgula, para remover dos nomes dos arquivos baixados (não diferencia maiúsculas de minúsculas).\nÚtil para limpar prefixos/sufixos comuns.\nExemplo: patreon, kemono, [HD], _final",
"skip_scope_files_text":"Escopo: Arquivos",
"skip_scope_files_tooltip":"Escopo de Pular Atual: Arquivos\n\nPula arquivos individuais se seus nomes contiverem alguma das 'Palavras a Pular'.\nExemplo: Pular palavras \"WIP, rascunho\".\n- Arquivo \"arte_WIP.jpg\" -> PULADO.\n- Arquivo \"arte_final.png\" -> BAIXADO (se outras condições forem atendidas).\n\nA publicação ainda é processada para outros arquivos não pulados.\nClique para alternar para: Ambos",
"skip_scope_posts_text":"Escopo: Publicações",
"skip_scope_posts_tooltip":"Escopo de Pular Atual: Publicações\n\nPula publicações inteiras se seus títulos contiverem alguma das 'Palavras a Pular'.\nTodos os arquivos de uma publicação pulada são ignorados.\nExemplo: Pular palavras \"prévia, anúncio\".\n- Publicação \"Anúncio emocionante!\" -> PULADA.\n- Publicação \"Obra de arte finalizada\" -> PROCESSADA (se outras condições forem atendidas).\n\nClique para alternar para: Arquivos",
"skip_scope_both_text":"Escopo: Ambos",
"skip_scope_both_tooltip":"Escopo de Pular Atual: Ambos (Publicações e depois Arquivos)\n\n1. Verifica o título da publicação: Se o título contiver uma palavra a pular, a publicação inteira é PULADA.\n2. Se o título da publicação estiver OK, então verifica os nomes dos arquivos individuais: Se um nome de arquivo contiver uma palavra a pular, apenas esse arquivo é PULADO.\nExemplo: Pular palavras \"WIP, rascunho\".\n- Publicação \"Rascunhos e WIPs\" (correspondência de título) -> PUBLICAÇÃO INTEIRA PULADA.\n- Publicação \"Atualização de Arte\" (título OK) com arquivos:\n  - \"personagem_WIP.jpg\" (correspondência de arquivo) -> PULADO.\n  - \"cena_final.png\" (arquivo OK) -> BAIXADO.\n\nClique para alternar para: Publicações",
"skip_scope_unknown_text":"Escopo: Desconhecido",
"skip_scope_unknown_tooltip":"O escopo das palavras a pular está em um estado desconhecido. Por favor, alterne ou reinicie.\n\nClique para alternar para: Publicações",
"language_change_title":"Idioma Alterado",
"language_change_message":"O idioma foi alterado. É necessário reiniciar para que todas as alterações tenham efeito total.",
"language_change_informative":"Deseja reiniciar a aplicação agora?",
"restart_now_button":"Reiniciar Agora",
"skip_zip_checkbox_label":"Pular .zip",
"skip_rar_checkbox_label":"Pular .rar",
"download_thumbnails_checkbox_label":"Baixar Apenas Miniaturas",
"scan_content_images_checkbox_label":"Escanear Conteúdo em Busca de Imagens",
"compress_images_checkbox_label":"Comprimir para WebP",
"separate_folders_checkbox_label":"Pastas Separadas por Nome/Título",
"subfolder_per_post_checkbox_label":"Subpasta por Publicação",
"use_cookie_checkbox_label":"Usar Cookie",
"use_multithreading_checkbox_base_label":"Usar Multithreading",
"show_external_links_checkbox_label":"Mostrar Links Externos no Log",
"manga_comic_mode_checkbox_label":"Modo Mangá/Quadrinhos",
"threads_label":"Threads:",
"start_download_button_text":"⬇️ Iniciar Download",
"start_download_button_tooltip":"Clique para iniciar o processo de download ou extração de links com as configurações atuais.",
"extract_links_button_text":"🔗 Extrair Links",
"pause_download_button_text":"⏸️ Pausar Download",
"pause_download_button_tooltip":"Clique para pausar o processo de download em andamento.",
"resume_download_button_text":"▶️ Retomar Download",
"resume_download_button_tooltip":"Clique para retomar o download.",
"cancel_button_text":"❌ Cancelar e Reiniciar UI",
"cancel_button_tooltip":"Clique para cancelar o processo de download/extração em andamento e reiniciar os campos da UI (preservando a URL e o Diretório).",
"error_button_text":"Erro",
"error_button_tooltip":"Ver arquivos pulados devido a erros e, opcionalmente, tentar novamente.",
"cancel_retry_button_text":"❌ Cancelar Retentativa",
"known_chars_label_text":"🎭 Shows/Personagens Conhecidos (para nomes de pastas):",
"open_known_txt_button_text":"Abrir Known.txt",
"known_chars_list_tooltip":"Esta lista contém nomes usados para a criação automática de pastas quando 'Pastas Separadas' está ativado\ne nenhum 'Filtrar por Personagem(ns)' específico é fornecido ou corresponde a uma publicação.\nAdicione nomes de séries, jogos ou personagens que você baixa com frequência.",
"open_known_txt_button_tooltip":"Abrir o arquivo 'Known.txt' em seu editor de texto padrão.\nO arquivo está localizado no diretório da aplicação.",
"add_char_button_text":"➕ Adicionar",
"add_char_button_tooltip":"Adicionar o nome do campo de entrada à lista 'Shows/Personagens Conhecidos'.",
"add_to_filter_button_text":"⤵️ Adicionar ao Filtro",
"add_to_filter_button_tooltip":"Selecione nomes da lista 'Shows/Personagens Conhecidos' para adicionar ao campo 'Filtrar por Personagem(ns)' acima.",
"delete_char_button_text":"🗑️ Excluir Selecionados",
"delete_char_button_tooltip":"Excluir os nomes selecionados da lista 'Shows/Personagens Conhecidos'.",
"progress_log_label_text":"📜 Log de Progresso:",
"radio_all_tooltip":"Baixar todos os tipos de arquivos encontrados nas publicações.",
"radio_images_tooltip":"Baixar apenas formatos de imagem comuns (JPG, PNG, GIF, WEBP, etc.).",
"radio_videos_tooltip":"Baixar apenas formatos de vídeo comuns (MP4, MKV, WEBM, MOV, etc.).",
"radio_only_archives_tooltip":"Baixar exclusivamente arquivos .zip e .rar. Outras opções específicas de arquivos são desativadas.",
"radio_only_audio_tooltip":"Baixar apenas formatos de áudio comuns (MP3, WAV, FLAC, etc.).",
"radio_only_links_tooltip":"Extrair e exibir links externos das descrições das publicações em vez de baixar arquivos.\nAs opções relacionadas ao download serão desativadas.",
"favorite_mode_checkbox_tooltip":"Habilite o Modo Favoritos para navegar por artistas/publicações salvos.\nIsso substituirá a entrada de URL por botões de seleção de Favoritos.",
"skip_zip_checkbox_tooltip":"Se marcado, arquivos de arquivamento .zip não serão baixados.\n(Desativado se 'Apenas Arquivos' for selecionado).",
"skip_rar_checkbox_tooltip":"Se marcado, arquivos de arquivamento .rar não serão baixados.\n(Desativado se 'Apenas Arquivos' for selecionado).",
"download_thumbnails_checkbox_tooltip":"Baixa pequenas imagens de visualização da API em vez de arquivos em tamanho real (se disponível).\nSe 'Escanear Conteúdo da Publicação em Busca de URLs de Imagens' também estiver marcado, este modo *apenas* baixará imagens encontradas pelo escaneamento de conteúdo (ignorando as miniaturas da API).",
"scan_content_images_checkbox_tooltip":"Se marcado, o downloader irá escanear o conteúdo HTML das publicações em busca de URLs de imagens (de tags <img> ou links diretos).\nIsso inclui a resolução de caminhos relativos de tags <img> para URLs completos.\nCaminhos relativos em tags <img> (ex: /data/image.jpg) serão resolvidos para URLs completos.\nÚtil para casos em que as imagens estão na descrição da publicação, mas não na lista de arquivos/anexos da API.",
"compress_images_checkbox_tooltip":"Comprimir imagens > 1.5MB para o formato WebP (requer Pillow).",
"use_subfolders_checkbox_tooltip":"Criar subpastas com base na entrada 'Filtrar por Personagem(ns)' ou nos títulos das publicações.\nUsa a lista 'Shows/Personagens Conhecidos' como fallback para nomes de pastas se nenhum filtro específico corresponder.\nHabilita a entrada 'Filtrar por Personagem(ns)' e 'Nome de Pasta Personalizado' para publicações únicas.",
"use_subfolder_per_post_checkbox_tooltip":"Cria uma subpasta para cada publicação. Se 'Pastas Separadas' também estiver ativado, ela fica dentro da pasta do personagem/título.",
"use_cookie_checkbox_tooltip":"Se marcado, tentará usar cookies de 'cookies.txt' (formato Netscape)\nno diretório da aplicação para solicitações.\nÚtil para acessar conteúdo que requer login no Kemono/Coomer.",
"cookie_text_input_tooltip":"Digite sua string de cookie diretamente.\nEla será usada se 'Usar Cookie' estiver marcado E 'cookies.txt' não for encontrado ou este campo não estiver vazio.\nO formato depende de como o backend o analisará (ex: 'nome1=valor1; nome2=valor2').",
"use_multithreading_checkbox_tooltip":"Habilita operações concorrentes. Consulte a entrada 'Threads' para mais detalhes.",
"thread_count_input_tooltip":"Número de operações concorrentes.\n- Publicação Única: Downloads de arquivos concorrentes (1-10 recomendado).\n- URL de Feed do Criador: Número de publicações a serem processadas simultaneamente (1-200 recomendado).\n  Arquivos dentro de cada publicação são baixados um por um por seu trabalhador.\nSe 'Usar Multithreading' não estiver marcado, 1 thread é usado.",
"external_links_checkbox_tooltip":"Se marcado, um painel de log secundário aparece abaixo do log principal para exibir links externos encontrados nas descrições das publicações.\n(Desativado se o modo 'Apenas Links' ou 'Apenas Arquivos' estiver ativo).",
"manga_mode_checkbox_tooltip":"Baixa as publicações da mais antiga para a mais nova e renomeia os arquivos com base no título da publicação (apenas para feeds de criadores).",
"multipart_on_button_text":"Multiparte: LIGADO",
"multipart_on_button_tooltip":"Download Multiparte: LIGADO\n\nHabilita o download de arquivos grandes em múltiplos segmentos simultaneamente.\n- Pode acelerar o download de arquivos grandes individuais (ex: vídeos).\n- Pode aumentar o uso de CPU/rede.\n- Para feeds com muitos arquivos pequenos, isso pode não oferecer benefícios de velocidade e pode tornar a UI/log congestionado.\n- Se o download multiparte falhar, ele tenta novamente como um único fluxo.\n\nClique para DESLIGAR.",
"multipart_off_button_text":"Multiparte: DESLIGADO",
"multipart_off_button_tooltip":"Download Multiparte: DESLIGADO\n\nTodos os arquivos são baixados usando um único fluxo.\n- Estável e funciona bem na maioria dos cenários, especialmente para muitos arquivos menores.\n- Arquivos grandes são baixados sequencialmente.\n\nClique para LIGAR (ver aviso).",
"reset_button_text":"🔄 Reiniciar",
"reset_button_tooltip":"Reiniciar todas as entradas e logs para o estado padrão (apenas quando ocioso).",
"progress_idle_text":"Progresso: Ocioso",
"missed_character_log_label_text":"🚫 Log de Personagens Perdidos:",
"creator_popup_title":"Seleção de Criador",
"creator_popup_search_placeholder":"Pesquisar por nome, serviço ou colar URL do criador...",
"creator_popup_add_selected_button":"Adicionar Selecionados",
"creator_popup_scope_characters_button":"Escopo: Personagens",
"creator_popup_scope_creators_button":"Escopo: Criadores",
"favorite_artists_button_text":"🖼️ Artistas Favoritos",
"favorite_artists_button_tooltip":"Navegue e baixe de seus artistas favoritos no Kemono.su/Coomer.su.",
"favorite_posts_button_text":"📄 Publicações Favoritas",
"favorite_posts_button_tooltip":"Navegue e baixe suas publicações favoritas do Kemono.su/Coomer.su.",
"favorite_scope_selected_location_text":"Escopo: Local Selecionado",
"favorite_scope_selected_location_tooltip":"Escopo de Download de Favoritos Atual: Local Selecionado\n\nTodos os artistas/publicações favoritos selecionados serão baixados para o 'Local de Download' principal especificado na UI.\nFiltros (personagem, palavras a pular, tipo de arquivo) serão aplicados globalmente a todo o conteúdo.\n\nClique para alterar para: Pastas de Artistas",
"favorite_scope_artist_folders_text":"Escopo: Pastas de Artistas",
"favorite_scope_artist_folders_tooltip":"Escopo de Download de Favoritos Atual: Pastas de Artistas\n\nPara cada artista/publicação favorito selecionado, uma nova subpasta (com o nome do artista) será criada dentro do 'Local de Download' principal.\nO conteúdo desse artista/publicação será baixado para sua subpasta específica.\nFiltros (personagem, palavras a pular, tipo de arquivo) serão aplicados *dentro* da pasta de cada artista.\n\nClique para alterar para: Local Selecionado",
"favorite_scope_unknown_text":"Escopo: Desconhecido",
"favorite_scope_unknown_tooltip":"O escopo de download de favoritos é desconhecido. Clique para alternar.",
"manga_style_post_title_text":"Nome: Título da Publicação",
"manga_style_original_file_text":"Nome: Arquivo Original",
"manga_style_date_based_text":"Nome: Baseado na Data",
"manga_style_title_global_num_text":"Nome: Título+Núm. Global",
"manga_style_unknown_text":"Nome: Estilo Desconhecido",
"fav_artists_dialog_title":"Artistas Favoritos",
"fav_artists_loading_status":"Carregando artistas favoritos...",
"fav_artists_search_placeholder":"Pesquisar artistas...",
"fav_artists_select_all_button":"Selecionar Todos",
"fav_artists_deselect_all_button":"Desmarcar Todos",
"fav_artists_download_selected_button":"Baixar Selecionados",
"fav_artists_cancel_button":"Cancelar",
"fav_artists_loading_from_source_status":"⏳ Carregando favoritos de {source_name}...",
"fav_artists_found_status":"{count} artista(s) favorito(s) encontrado(s) no total.",
"fav_artists_none_found_status":"Nenhum artista favorito encontrado no Kemono.su ou Coomer.su.",
"fav_artists_failed_status":"Falha ao buscar favoritos.",
"fav_artists_cookies_required_status":"Erro: Cookies habilitados, mas não puderam ser carregados para nenhuma fonte.",
"fav_artists_no_favorites_after_processing":"Nenhum artista favorito encontrado após o processamento.",
"fav_artists_no_selection_title":"Nenhuma Seleção",
"fav_artists_no_selection_message":"Por favor, selecione pelo menos um artista para baixar.",
"fav_posts_dialog_title":"Publicações Favoritas",
"fav_posts_loading_status":"Carregando publicações favoritas...",
"fav_posts_search_placeholder":"Pesquisar publicações (título, criador, ID, serviço)...",
"fav_posts_select_all_button":"Selecionar Todos",
"fav_posts_deselect_all_button":"Desmarcar Todos",
"fav_posts_download_selected_button":"Baixar Selecionados",
"fav_posts_cancel_button":"Cancelar",
"fav_posts_cookies_required_error":"Erro: Cookies são necessários para publicações favoritas, mas não puderam ser carregados.",
"fav_posts_auth_failed_title":"Falha na Autenticação (Publicações)",
"fav_posts_auth_failed_message":"Não foi possível buscar favoritos{domain_specific_part} devido a um erro de autorização:\n\n{error_message}\n\nIsso geralmente significa que seus cookies estão ausentes, inválidos ou expirados para o site. Verifique a configuração de seus cookies.",
"fav_posts_fetch_error_title":"Erro ao Buscar",
"fav_posts_fetch_error_message":"Erro ao buscar favoritos de {domain}{error_message_part}",
"fav_posts_no_posts_found_status":"Nenhuma publicação favorita encontrada.",
"fav_posts_found_status":"{count} publicação(ões) favorita(s) encontrada(s).",
"fav_posts_display_error_status":"Erro ao exibir publicações: {error}",
"fav_posts_ui_error_title":"Erro de UI",
"fav_posts_ui_error_message":"Não foi possível exibir as publicações favoritas: {error}",
"fav_posts_auth_failed_message_generic":"Não foi possível buscar favoritos{domain_specific_part} devido a um erro de autorização. Isso geralmente significa que seus cookies estão ausentes, inválidos ou expirados para o site. Verifique a configuração de seus cookies.",
"key_fetching_fav_post_list_init":"Buscando lista de publicações favoritas...",
"key_fetching_from_source_kemono_su":"Buscando favoritos do Kemono.su...",
"key_fetching_from_source_coomer_su":"Buscando favoritos do Coomer.su...",
"fav_posts_fetch_cancelled_status":"Busca de publicações favoritas cancelada.",
"known_names_filter_dialog_title":"Adicionar Nomes Conhecidos ao Filtro",
"known_names_filter_search_placeholder":"Pesquisar nomes...",
"known_names_filter_select_all_button":"Selecionar Todos",
"known_names_filter_deselect_all_button":"Desmarcar Todos",
"known_names_filter_add_selected_button":"Adicionar Selecionados",
"error_files_dialog_title":"Arquivos Pulados Devido a Erros",
"error_files_no_errors_label":"Nenhum arquivo foi registrado como pulado devido a erros na última sessão ou após novas tentativas.",
"error_files_found_label":"Os seguintes {count} arquivo(s) foram pulados devido a erros de download:",
"error_files_select_all_button":"Selecionar Todos",
"error_files_retry_selected_button":"Tentar Novamente os Selecionados",
"error_files_export_urls_button":"Exportar URLs para .txt",
"error_files_no_selection_retry_message":"Por favor, selecione pelo menos um arquivo para tentar novamente.",
"error_files_no_errors_export_title":"Sem Erros",
"error_files_no_errors_export_message":"Não há URLs de arquivos de erro para exportar.",
"error_files_no_urls_found_export_title":"Nenhuma URL Encontrada",
"error_files_no_urls_found_export_message":"Não foi possível extrair nenhuma URL da lista de arquivos de erro para exportar.",
"error_files_save_dialog_title":"Salvar URLs de Arquivos de Erro",
"error_files_export_success_title":"Exportação Bem-sucedida",
"error_files_export_success_message":"{count} entradas exportadas com sucesso para:\n{filepath}",
"error_files_export_error_title":"Erro de Exportação",
"error_files_export_error_message":"Não foi possível exportar os links dos arquivos: {error}",
"export_options_dialog_title":"Opções de Exportação",
"export_options_description_label":"Escolha o formato para exportar os links dos arquivos de erro:",
"export_options_radio_link_only":"Link por linha (apenas URL)",
"export_options_radio_link_only_tooltip":"Exporta apenas a URL de download direto para cada arquivo com falha, uma URL por linha.",
"export_options_radio_with_details":"Exportar com detalhes (URL [Publicação, Informações do arquivo])",
"export_options_radio_with_details_tooltip":"Exporta a URL seguida por detalhes como Título da Publicação, ID da Publicação e Nome de Arquivo Original entre colchetes.",
"export_options_export_button":"Exportar",
"no_errors_logged_title":"Nenhum Erro Registrado",
"no_errors_logged_message":"Nenhum arquivo foi registrado como pulado devido a erros na última sessão ou após novas tentativas.",
"progress_initializing_text":"Progresso: Inicializando...",
"progress_posts_text":"Progresso: {processed_posts} / {total_posts} publicações ({progress_percent:.1f}%)",
"progress_processing_post_text":"Progresso: Processando publicação {processed_posts}...",
"progress_starting_text":"Progresso: Iniciando...",
"downloading_file_known_size_text":"Baixando '{filename}' ({downloaded_mb:.1f}MB / {total_mb:.1f}MB)",
"downloading_file_unknown_size_text":"Baixando '{filename}' ({downloaded_mb:.1f}MB)",
"downloading_multipart_text":"DL '{filename}...': {downloaded_mb:.1f}/{total_mb:.1f} MB ({parts} partes @ {speed:.2f} MB/s)",
"downloading_multipart_initializing_text":"Arquivo: {filename} - Inicializando partes...",
"status_completed":"Concluído",
"status_cancelled_by_user":"Cancelado pelo usuário",
"files_downloaded_label":"baixados",
"files_skipped_label":"pulados",
"retry_finished_text":"Retentativa Concluída",
"succeeded_text":"Bem-sucedido",
"failed_text":"Falhou",
"ready_for_new_task_text":"Pronto para nova tarefa.",
"fav_mode_active_label_text":"Escolha os filtros abaixo antes de selecionar os seus favoritos.",
"export_links_button_text":"Exportar Links",
"download_extracted_links_button_text":"Baixar",
"download_selected_button_text":"Baixar Selecionados",
"link_input_placeholder_text":"ex: https://kemono.su/patreon/user/12345 ou .../post/98765",
"link_input_tooltip_text":"Digite a URL completa de uma página de criador do Kemono/Coomer ou de uma publicação específica.\nExemplo (Criador): https://kemono.su/patreon/user/12345\nExemplo (Publicação): https://kemono.su/patreon/user/12345/post/98765",
"dir_input_placeholder_text":"Selecione a pasta onde os downloads serão salvos",
"dir_input_tooltip_text":"Digite ou procure a pasta principal onde todo o conteúdo baixado será salvo.\nEste campo é obrigatório, a menos que o modo 'Apenas Links' esteja selecionado.",
"character_input_placeholder_text":"ex: Tifa, Aerith, (Cloud, Zack)",
"custom_folder_input_placeholder_text":"Opcional: Salvar esta publicação em uma pasta específica",
"custom_folder_input_tooltip_text":"Se você estiver baixando a URL de uma única publicação E 'Pastas Separadas por Nome/Título' estiver habilitado,\nvocê pode inserir um nome personalizado aqui para a pasta de download dessa publicação.\nExemplo: Minha Cena Favorita",
"skip_words_input_placeholder_text":"ex: WM, WIP, rascunho, prévia",
"remove_from_filename_input_placeholder_text":"ex: patreon, HD",
"cookie_text_input_placeholder_no_file_selected_text":"String de cookie (se nenhum cookies.txt for selecionado)",
"cookie_text_input_placeholder_with_file_selected_text":"Usando o arquivo de cookie selecionado (ver Procurar...)",
"character_search_input_placeholder_text":"Pesquisar personagens...",
"character_search_input_tooltip_text":"Digite aqui para filtrar a lista de shows/personagens conhecidos abaixo.",
"new_char_input_placeholder_text":"Adicionar novo nome de show/personagem",
"new_char_input_tooltip_text":"Digite um novo nome de show, jogo ou personagem para adicionar à lista acima.",
"link_search_input_placeholder_text":"Pesquisar Links...",
"link_search_input_tooltip_text":"No modo 'Apenas Links', digite aqui para filtrar os links exibidos por texto, URL ou plataforma.",
"manga_date_prefix_input_placeholder_text":"Prefixo para Nomes de Arquivo de Mangá",
"manga_date_prefix_input_tooltip_text":"Prefixo opcional para nomes de arquivo de mangá 'Baseado na Data' ou 'Arquivo Original' (ex: 'Nome da Série').\nSe vazio, os arquivos serão nomeados de acordo com o estilo sem um prefixo.",
"log_display_mode_links_view_text":"🔗 Visualização de Links",
"log_display_mode_progress_view_text":"⬇️ Visualização de Progresso",
"download_external_links_dialog_title":"Baixar Links Externos Selecionados",
"select_all_button_text":"Selecionar Todos",
"deselect_all_button_text":"Desmarcar Todos",
"cookie_browse_button_tooltip":"Procure por um arquivo de cookie (formato Netscape, geralmente cookies.txt).\nEle será usado se 'Usar Cookie' estiver marcado e o campo de texto acima estiver vazio.",
"page_range_label_text":"Intervalo de Páginas:",
"start_page_input_placeholder":"Início",
"start_page_input_tooltip":"Para URLs de criadores: Especifique o número da página inicial para baixar (ex: 1, 2, 3).\nDeixe em branco ou defina como 1 para começar da primeira página.\nDesativado para URLs de publicações únicas ou no Modo Mangá/Quadrinhos.",
"page_range_to_label_text":"a",
"end_page_input_placeholder":"Fim",
"end_page_input_tooltip":"Para URLs de criadores: Especifique o número da página final para baixar (ex: 5, 10).\nDeixe em branco para baixar todas as páginas a partir da página inicial.\nDesativado para URLs de publicações únicas ou no Modo Mangá/Quadrinhos.",
"known_names_help_button_tooltip_text":"Abrir o guia de recursos da aplicação.",
"future_settings_button_tooltip_text":"Abrir as configurações da aplicação (Tema, Idioma, etc.).",
"link_search_button_tooltip_text":"Filtrar links exibidos",
"confirm_add_all_dialog_title":"Confirmar Adição de Novos Nomes",
"confirm_add_all_info_label":"Os seguintes novos nomes/grupos da sua entrada 'Filtrar por Personagem(ns)' não estão em 'Known.txt'.\nAdicioná-los pode melhorar a organização de pastas para futuros downloads.\n\nRevise a lista e escolha uma ação:",
"confirm_add_all_select_all_button":"Selecionar Todos",
"confirm_add_all_deselect_all_button":"Desmarcar Todos",
"confirm_add_all_add_selected_button":"Adicionar Selecionados ao Known.txt",
"confirm_add_all_skip_adding_button":"Pular Adição Destes",
"confirm_add_all_cancel_download_button":"Cancelar Download",
"cookie_help_dialog_title":"Instruções do Arquivo de Cookie",
"cookie_help_instruction_intro":"<p>Para usar cookies, você normalmente precisa de um arquivo <b>cookies.txt</b> do seu navegador.</p>",
"cookie_help_how_to_get_title":"<p><b>Como obter o cookies.txt:</b></p>",
"cookie_help_step1_extension_intro":"<li>Instale a extensão 'Get cookies.txt LOCALLY' para seu navegador baseado em Chrome:<br><a href=\"https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc\" style=\"color: #87CEEB;\">Obter Get cookies.txt LOCALLY na Chrome Web Store</a></li>",
"cookie_help_step2_login":"<li>Vá para o site (ex: kemono.su ou coomer.su) e faça login, se necessário.</li>",
"cookie_help_step3_click_icon":"<li>Clique no ícone da extensão na barra de ferramentas do seu navegador.</li>",
"cookie_help_step4_export":"<li>Clique em um botão 'Exportar' (ex: \"Exportar Como\", \"Exportar cookies.txt\" - a redação exata pode variar dependendo da versão da extensão).</li>",
"cookie_help_step5_save_file":"<li>Salve o arquivo <code>cookies.txt</code> baixado no seu computador.</li>",
"cookie_help_step6_app_intro":"<li>Nesta aplicação:<ul>",
"cookie_help_step6a_checkbox":"<li>Certifique-se de que a caixa de seleção 'Usar Cookie' está marcada.</li>",
"cookie_help_step6b_browse":"<li>Clique no botão 'Procurar...' ao lado do campo de texto do cookie.</li>",
"cookie_help_step6c_select":"<li>Selecione o arquivo <code>cookies.txt</code> que você acabou de salvar.</li></ul></li>",
"cookie_help_alternative_paste":"<p>Alternativamente, algumas extensões podem permitir que você copie a string do cookie diretamente. Se for o caso, você pode colá-la no campo de texto em vez de procurar um arquivo.</p>",
"cookie_help_proceed_without_button":"Baixar sem Cookies",
"empty_popup_button_tooltip_text": "Abrir Seleção de Criador (Procurar creators.json)",
"cookie_help_cancel_download_button":"Cancelar Download",
"character_input_tooltip":"Digite os nomes dos personagens (separados por vírgula). Suporta agrupamento avançado e afeta a nomenclatura de pastas se 'Pastas Separadas' estiver habilitado.\n\nExemplos:\n- Nami → Corresponde a 'Nami', cria a pasta 'Nami'.\n- (Ulti, Vivi) → Corresponde a um dos dois, pasta 'Ulti Vivi', adiciona ambos ao Known.txt separadamente.\n- (Boa, Hancock)~ → Corresponde a um dos dois, pasta 'Boa Hancock', adiciona como um grupo no Known.txt.\n\nOs nomes são tratados como apelidos para correspondência.\n\nModos de Filtro (o botão alterna):\n- Arquivos: Filtra por nome de arquivo.\n- Título: Filtra por título da publicação.\n- Ambos: Título primeiro, depois nome de arquivo.\n- Comentários (Beta): Nome de arquivo primeiro, depois comentários da publicação.",
"tour_dialog_title":"Bem-vindo ao Kemono Downloader!",
"tour_dialog_never_show_checkbox":"Não mostrar este tour novamente",
"tour_dialog_skip_button":"Pular Tour",
"tour_dialog_back_button":"Voltar",
"tour_dialog_next_button":"Próximo",
"tour_dialog_finish_button":"Concluir",
"tour_dialog_step1_title":"👋 Bem-vindo!",
"tour_dialog_step1_content":"Olá! Este rápido tour irá guiá-lo pelas principais funcionalidades do Kemono Downloader, incluindo atualizações recentes como filtragem aprimorada, melhorias no modo mangá e gerenciamento de cookies.\n<ul>\n<li>Meu objetivo é ajudá-lo a baixar facilmente conteúdo do <b>Kemono</b> e do <b>Coomer</b>.</li><br>\n<li><b>🎨 Botão de Seleção de Criador:</b> Ao lado da entrada de URL, clique no ícone da paleta para abrir um diálogo. Navegue e selecione criadores do seu arquivo <code>creators.json</code> para adicionar rapidamente seus nomes à entrada de URL.</li><br>\n<li><b>Dica Importante: App '(Não Respondendo)'?</b><br>\nApós clicar em 'Iniciar Download', especialmente para feeds de criadores grandes ou com muitos threads, a aplicação pode ser exibida temporariamente como '(Não Respondendo)'. Seu sistema operacional (Windows, macOS, Linux) pode até sugerir que você 'Finalize o Processo' ou 'Force o Encerramento'.<br>\n<b>Por favor, seja paciente!</b> O app geralmente ainda está trabalhando duro em segundo plano. Antes de forçar o fechamento, tente verificar o 'Local de Download' escolhido em seu explorador de arquivos. Se você vir novas pastas sendo criadas ou arquivos aparecendo, significa que o download está progredindo corretamente. Dê um tempo para que ele volte a responder.</li><br>\n<li>Use os botões <b>Próximo</b> e <b>Voltar</b> para navegar.</li><br>\n<li>Muitas opções têm dicas de ferramentas se você passar o mouse sobre elas para mais detalhes.</li><br>\n<li>Clique em <b>Pular Tour</b> para fechar este guia a qualquer momento.</li><br>\n<li>Marque <b>'Não mostrar este tour novamente'</b> se não quiser vê-lo em futuras inicializações.</li>\n</ul>",
"tour_dialog_step2_title":"① Primeiros Passos",
"tour_dialog_step2_content":"Vamos começar com o básico para o download:\n<ul>\n<li><b>🔗 URL do Criador/Post do Kemono:</b><br>\nCole o endereço web completo (URL) de uma página de criador (ex: <i>https://kemono.su/patreon/user/12345</i>)\nou de uma publicação específica (ex: <i>.../post/98765</i>).<br>\nou de um criador do Coomer (ex: <i>https://coomer.su/onlyfans/user/artistname</i>)</li><br>\n<li><b>📁 Local de Download:</b><br>\nClique em 'Procurar...' para escolher uma pasta em seu computador onde todos os arquivos baixados serão salvos.\nEste campo é obrigatório, a menos que você esteja usando o modo 'Apenas Links'.</li><br>\n<li><b>📄 Intervalo de Páginas (apenas URL de criador):</b><br>\nSe estiver baixando de uma página de criador, você pode especificar um intervalo de páginas para buscar (ex: páginas 2 a 5).\nDeixe em branco para todas as páginas. Isso é desativado para URLs de publicações únicas ou quando o <b>Modo Mangá/Quadrinhos</b> está ativo.</li>\n</ul>",
"tour_dialog_step3_title":"② Filtrando Downloads",
"tour_dialog_step3_content":"Refine o que você baixa com estes filtros (a maioria está desativada nos modos 'Apenas Links' ou 'Apenas Arquivos'):\n<ul>\n<li><b>🎯 Filtrar por Personagem(ns):</b><br>\nDigite nomes de personagens, separados por vírgula (ex: <i>Tifa, Aerith</i>). Agrupe apelidos para um nome de pasta combinado: <i>(apelido1, apelido2, apelido3)</i> se torna a pasta 'apelido1 apelido2 apelido3' (após a limpeza). Todos os nomes no grupo são usados como apelidos para correspondência.<br>\nO botão <b>'Filtro: [Tipo]'</b> (ao lado desta entrada) alterna como este filtro se aplica:\n<ul><li><i>Filtro: Arquivos:</i> Verifica nomes de arquivos individuais. Uma publicação é mantida se algum arquivo corresponder; apenas os arquivos correspondentes são baixados. A nomenclatura de pastas usa o personagem do nome do arquivo correspondente (se 'Pastas Separadas' estiver ativado).</li><br>\n<li><i>Filtro: Título:</i> Verifica títulos de publicações. Todos os arquivos de uma publicação correspondente são baixados. A nomenclatura de pastas usa o personagem do título da publicação correspondente.</li>\n<li><b>⤵️ Botão Adicionar ao Filtro (Nomes Conhecidos):</b> Ao lado do botão 'Adicionar' para Nomes Conhecidos (ver Passo 5), isso abre um pop-up. Selecione nomes da sua lista <code>Known.txt</code> através de caixas de seleção (com uma barra de pesquisa) para adicioná-los rapidamente ao campo 'Filtrar por Personagem(ns)'. Nomes agrupados como <code>(Boa, Hancock)</code> do Known.txt serão adicionados como <code>(Boa, Hancock)~</code> ao filtro.</li><br>\n<li><i>Filtro: Ambos:</i> Verifica o título da publicação primeiro. Se corresponder, todos os arquivos são baixados. Se não, verifica os nomes dos arquivos, e apenas os arquivos correspondentes são baixados. A nomenclatura de pastas prioriza a correspondência de título, depois a correspondência de arquivo.</li><br>\n<li><i>Filtro: Comentários (Beta):</i> Verifica os nomes dos arquivos primeiro. Se um arquivo corresponder, todos os arquivos da publicação são baixados. Se não houver correspondência de arquivo, então verifica os comentários da publicação. Se um comentário corresponder, todos os arquivos são baixados. (Usa mais solicitações de API). A nomenclatura de pastas prioriza a correspondência de arquivo, depois a correspondência de comentário.</li></ul>\nEste filtro também influencia a nomenclatura de pastas se 'Pastas Separadas por Nome/Título' estiver habilitado.</li><br>\n<li><b>🚫 Ignorar com Palavras:</b><br>\nDigite palavras, separadas por vírgula (ex: <i>WIP, rascunho, prévia</i>).\nO botão <b>'Escopo: [Tipo]'</b> (ao lado desta entrada) alterna como este filtro se aplica:\n<ul><li><i>Escopo: Arquivos:</i> Pula arquivos se seus nomes contiverem alguma dessas palavras.</li><br>\n<li><i>Escopo: Publicações:</i> Pula publicações inteiras se seus títulos contiverem alguma dessas palavras.</li><br>\n<li><i>Escopo: Ambos:</i> Aplica tanto o pulo de arquivo quanto de título de publicação (publicação primeiro, depois arquivos).</li></ul></li><br>\n<li><b>Filtrar Arquivos (Botões de Rádio):</b> Escolha o que baixar:\n<ul>\n<li><i>Todos:</i> Baixa todos os tipos de arquivos encontrados.</li><br>\n<li><i>Imagens/GIFs:</i> Apenas formatos de imagem comuns e GIFs.</li><br>\n<li><i>Vídeos:</i> Apenas formatos de vídeo comuns.</li><br>\n<li><b><i>📦 Apenas Arquivos:</i></b> Baixa exclusivamente arquivos <b>.zip</b> e <b>.rar</b>. Quando selecionado, as caixas de seleção 'Pular .zip' e 'Pular .rar' são automaticamente desativadas e desmarcadas. 'Mostrar Links Externos' também é desativado.</li><br>\n<li><i>🎧 Apenas Áudio:</i> Apenas formatos de áudio comuns (MP3, WAV, FLAC, etc.).</li><br>\n<li><i>🔗 Apenas Links:</i> Extrai e exibe links externos das descrições das publicações em vez de baixar arquivos. As opções relacionadas ao download e 'Mostrar Links Externos' são desativadas.</li>\n</ul></li>\n</ul>",
"tour_dialog_step4_title":"③ Modo Favoritos (Download Alternativo)",
"tour_dialog_step4_content":"A aplicação oferece um 'Modo Favoritos' para baixar conteúdo de artistas que você favoritou no Kemono.su.\n<ul>\n<li><b>⭐ Caixa de Seleção Modo Favoritos:</b><br>\nLocalizada ao lado do botão de rádio '🔗 Apenas Links'. Marque esta caixa para ativar o Modo Favoritos.</li><br>\n<li><b>O que Acontece no Modo Favoritos:</b>\n<ul><li>A área de entrada '🔗 URL do Criador/Post do Kemono' é substituída por uma mensagem indicando que o Modo Favoritos está ativo.</li><br>\n<li>Os botões padrão 'Iniciar Download', 'Pausar', 'Cancelar' são substituídos pelos botões '🖼️ Artistas Favoritos' e '📄 Publicações Favoritas' (Nota: 'Publicações Favoritas' está planejado para o futuro).</li><br>\n<li>A opção '🍪 Usar Cookie' é automaticamente habilitada e bloqueada, pois os cookies são necessários para buscar seus favoritos.</li></ul></li><br>\n<li><b>🖼️ Botão Artistas Favoritos:</b><br>\nClique aqui para abrir um diálogo listando seus artistas favoritos do Kemono.su. Você pode selecionar um ou mais artistas para baixar.</li><br>\n<li><b>Escopo de Download de Favoritos (Botão):</b><br>\nEste botão (ao lado de 'Publicações Favoritas') controla onde os favoritos selecionados são baixados:\n<ul><li><i>Escopo: Local Selecionado:</i> Todos os artistas selecionados são baixados para o 'Local de Download' principal que você definiu. Os filtros se aplicam globalmente.</li><br>\n<li><i>Escopo: Pastas de Artistas:</i> Uma subpasta (com o nome do artista) é criada em seu 'Local de Download' principal para cada artista selecionado. O conteúdo desse artista vai para sua pasta específica. Os filtros se aplicam dentro da pasta de cada artista.</li></ul></li><br>\n<li><b>Filtros no Modo Favoritos:</b><br>\nAs opções 'Filtrar por Personagem(ns)', 'Ignorar com Palavras' e 'Filtrar Arquivos' ainda se aplicam ao conteúdo baixado de seus artistas favoritos selecionados.</li>\n</ul>",
"tour_dialog_step5_title":"④ Ajuste Fino de Downloads",
"tour_dialog_step5_content":"Mais opções para personalizar seus downloads:\n<ul>\n<li><b>Pular .zip / Pular .rar:</b> Marque estas caixas para evitar o download desses tipos de arquivos de arquivamento.\n<i>(Nota: Eles são desativados e ignorados se o modo de filtro '📦 Apenas Arquivos' for selecionado).</i></li><br>\n<li><b>✂️ Remover Palavras do nome:</b><br>\nDigite palavras, separadas por vírgula (ex: <i>patreon, [HD]</i>), para remover dos nomes dos arquivos baixados (não diferencia maiúsculas de minúsculas).</li><br>\n<li><b>Baixar Apenas Miniaturas:</b> Baixa pequenas imagens de visualização em vez de arquivos em tamanho real (se disponível).</li><br>\n<li><b>Comprimir Imagens Grandes:</b> Se a biblioteca 'Pillow' estiver instalada, imagens maiores que 1.5MB serão convertidas para o formato WebP se a versão WebP for significativamente menor.</li><br>\n<li><b>🗄️ Nome de Pasta Personalizado (Apenas Publicação Única):</b><br>\nSe você estiver baixando uma URL de publicação específica E 'Pastas Separadas por Nome/Título' estiver habilitado,\nvocê pode inserir um nome personalizado aqui para a pasta de download dessa publicação.</li><br>\n<li><b>🍪 Usar Cookie:</b> Marque esta caixa para usar cookies para solicitações. Você pode:\n<ul><li>Digitar uma string de cookie diretamente no campo de texto (ex: <i>nome1=valor1; nome2=valor2</i>).</li><br>\n<li>Clicar em 'Procurar...' para selecionar um arquivo <i>cookies.txt</i> (formato Netscape). O caminho aparecerá no campo de texto.</li></ul>\nIsso é útil para acessar conteúdo que requer login. O campo de texto tem precedência se preenchido.\nSe 'Usar Cookie' estiver marcado, mas tanto o campo de texto quanto o arquivo procurado estiverem vazios, ele tentará carregar 'cookies.txt' do diretório da aplicação.</li>\n</ul>",
"tour_dialog_step6_title":"⑤ Organização e Desempenho",
"tour_dialog_step6_content":"Organize seus downloads e gerencie o desempenho:\n<ul>\n<li><b>⚙️ Pastas Separadas por Nome/Título:</b> Cria subpastas com base na entrada 'Filtrar por Personagem(ns)' ou nos títulos das publicações (pode usar a lista <b>Known.txt</b> como fallback para nomes de pastas).</li><br>\n<li><b>Subpasta por Publicação:</b> Se 'Pastas Separadas' estiver ativado, isso cria uma subpasta adicional para <i>cada publicação individual</i> dentro da pasta principal do personagem/título.</li><br>\n<li><b>🚀 Usar Multithreading (Threads):</b> Habilita operações mais rápidas. O número na entrada 'Threads' significa:\n<ul><li>Para <b>Feeds de Criadores:</b> Número de publicações a serem processadas simultaneamente. Arquivos dentro de cada publicação são baixados sequencialmente por seu trabalhador (a menos que a nomenclatura de mangá 'Baseada na Data' esteja ativada, o que força 1 trabalhador de publicação).</li><br>\n<li>Para <b>URLs de Publicações Únicas:</b> Número de arquivos a serem baixados simultaneamente dessa única publicação.</li></ul>\nSe não estiver marcado, 1 thread é usado. Contagens altas de threads (ex: >40) podem exibir um aviso.</li><br>\n<li><b>Alternador de Download Multiparte (canto superior direito da área de log):</b><br>\nO botão <b>'Multiparte: [LIGADO/DESLIGADO]'</b> permite habilitar/desabilitar downloads multissegmento para arquivos grandes individuais.\n<ul><li><b>LIGADO:</b> Pode acelerar o download de arquivos grandes (ex: vídeos), mas pode aumentar a instabilidade da UI ou o spam de log com muitos arquivos pequenos. Um aviso aparece ao habilitar. Se um download multiparte falhar, ele tenta novamente como um único fluxo.</li><br>\n<li><b>DESLIGADO (Padrão):</b> Os arquivos são baixados em um único fluxo.</li></ul>\nIsso é desativado se o modo 'Apenas Links' ou 'Apenas Arquivos' estiver ativo.</li><br>\n<li><b>📖 Modo Mangá/Quadrinhos (apenas URL de criador):</b> Adaptado para conteúdo sequencial.\n<ul>\n<li>Baixa as publicações da <b>mais antiga para a mais nova</b>.</li><br>\n<li>A entrada 'Intervalo de Páginas' é desativada, pois todas as publicações são buscadas.</li><br>\n<li>Um <b>botão de alternância de estilo de nome de arquivo</b> (ex: 'Nome: Título da Publicação') aparece no canto superior direito da área de log quando este modo está ativo para um feed de criador. Clique nele para alternar entre os estilos de nomenclatura:\n<ul>\n<li><b><i>Nome: Título da Publicação (Padrão):</i></b> O primeiro arquivo em uma publicação é nomeado com base no título limpo da publicação (ex: 'Meu Capítulo 1.jpg'). Arquivos subsequentes na *mesma publicação* tentarão manter seus nomes de arquivo originais (ex: 'pagina_02.png', 'arte_bonus.jpg'). Se a publicação tiver apenas um arquivo, ele será nomeado com base no título da publicação. Isso é geralmente recomendado para a maioria dos mangás/quadrinhos.</li><br>\n<li><b><i>Nome: Arquivo Original:</i></b> Todos os arquivos tentam manter seus nomes de arquivo originais. Um prefixo opcional (ex: 'MinhaSérie_') pode ser inserido no campo de entrada que aparece ao lado do botão de estilo. Exemplo: 'MinhaSérie_ArquivoOriginal.jpg'.</li><br>\n<li><b><i>Nome: Título+Núm. Global (Título da Publicação + Numeração Global):</i></b> Todos os arquivos em todas as publicações na sessão de download atual são nomeados sequencialmente usando o título limpo da publicação como prefixo, seguido por um contador global. Por exemplo: Publicação 'Capítulo 1' (2 arquivos) -> 'Capítulo 1_001.jpg', 'Capítulo 1_002.png'. A próxima publicação, 'Capítulo 2' (1 arquivo), continuaria a numeração -> 'Capítulo 2_003.jpg'. O multithreading para processamento de publicações é desativado automaticamente para este estilo para garantir a numeração global correta.</li><br>\n<li><b><i>Nome: Baseado na Data:</i></b> Os arquivos são nomeados sequencialmente (001.ext, 002.ext, ...) com base na ordem de publicação dos posts. Um prefixo opcional (ex: 'MinhaSérie_') pode ser inserido no campo de entrada que aparece ao lado do botão de estilo. Exemplo: 'MinhaSérie_001.jpg'. O multithreading para processamento de publicações é desativado automaticamente para este estilo.</li>\n</ul>\n</li><br>\n<li>Para obter os melhores resultados com os estilos 'Nome: Título da Publicação', 'Nome: Título+Núm. Global' ou 'Nome: Baseado na Data', use o campo 'Filtrar por Personagem(ns)' com o título do mangá/série para a organização de pastas.</li>\n</ul></li><br>\n<li><b>🎭 Known.txt para Organização Inteligente de Pastas:</b><br>\n<code>Known.txt</code> (no diretório da aplicação) permite um controle refinado sobre a organização automática de pastas quando 'Pastas Separadas por Nome/Título' está ativado.\n<ul>\n<li><b>Como Funciona:</b> Cada linha em <code>Known.txt</code> é uma entrada.\n<ul><li>Uma linha simples como <code>Minha Série Incrível</code> significa que o conteúdo que corresponder a isso irá para uma pasta chamada \"Minha Série Incrível\".</li><br>\n<li>Uma linha agrupada como <code>(Personagem A, Pers A, Nome Alt A)</code> significa que o conteúdo que corresponder a \"Personagem A\", \"Pers A\" OU \"Nome Alt A\" irá TODO para uma única pasta chamada \"Personagem A Pers A Nome Alt A\" (após a limpeza). Todos os termos entre parênteses se tornam apelidos para essa pasta.</li></ul></li>\n<li><b>Fallback Inteligente:</b> Quando 'Pastas Separadas por Nome/Título' está ativo, e se uma publicação não corresponder a nenhuma entrada específica de 'Filtrar por Personagem(ns)', o downloader consulta <code>Known.txt</code> para encontrar um nome principal correspondente para a criação da pasta.</li><br>\n<li><b>Gerenciamento Fácil de Usar:</b> Adicione nomes simples (não agrupados) através da lista da UI abaixo. Para edição avançada (como criar/modificar apelidos agrupados), clique em <b>'Abrir Known.txt'</b> para editar o arquivo em seu editor de texto. O app o recarrega no próximo uso ou inicialização.</li>\n</ul>\n</li>\n</ul>",
"tour_dialog_step7_title":"⑥ Erros Comuns e Solução de Problemas",
"tour_dialog_step7_content":"Às vezes, os downloads podem encontrar problemas. Aqui estão alguns comuns:\n<ul>\n<li><b>Dica de Ferramenta de Entrada de Personagem:</b><br>\nDigite nomes de personagens, separados por vírgula (ex: <i>Tifa, Aerith</i>).<br>\nAgrupe apelidos para um nome de pasta combinado: <i>(apelido1, apelido2, apelido3)</i> se torna a pasta 'apelido1 apelido2 apelido3'.<br>\nTodos os nomes no grupo são usados como apelidos para o conteúdo correspondente.<br><br>\nO botão 'Filtro: [Tipo]' ao lado desta entrada alterna como este filtro se aplica:<br>\n- Filtro: Arquivos: Verifica nomes de arquivos individuais. Apenas os arquivos correspondentes são baixados.<br>\n- Filtro: Título: Verifica títulos de publicações. Todos os arquivos de uma publicação correspondente são baixados.<br>\n- Filtro: Ambos: Verifica o título da publicação primeiro. Se não houver correspondência, verifica os nomes dos arquivos.<br>\n- Filtro: Comentários (Beta): Verifica os nomes dos arquivos primeiro. Se não houver correspondência, verifica os comentários da publicação.<br><br>\nEste filtro também influencia a nomenclatura de pastas se 'Pastas Separadas por Nome/Título' estiver habilitado.</li><br>\n<li><b>502 Bad Gateway / 503 Service Unavailable / 504 Gateway Timeout:</b><br>\nIsso geralmente indica problemas temporários do lado do servidor com o Kemono/Coomer. O site pode estar sobrecarregado, em manutenção ou com problemas.<br>\n<b>Solução:</b> Espere um pouco (ex: 30 minutos a algumas horas) e tente novamente mais tarde. Verifique o site diretamente em seu navegador.</li><br>\n<li><b>Conexão Perdida / Conexão Recusada / Timeout (durante o download de arquivos):</b><br>\nIsso pode acontecer devido à sua conexão com a internet, instabilidade do servidor ou se o servidor interromper a conexão para um arquivo grande.<br>\n<b>Solução:</b> Verifique sua internet. Tente reduzir o número de 'Threads' se estiver alto. O app pode solicitar que você tente novamente alguns arquivos com falha no final de uma sessão.</li><br>\n<li><b>Erro IncompleteRead:</b><br>\nO servidor enviou menos dados do que o esperado. Muitas vezes um problema temporário de rede ou de servidor.<br>\n<b>Solução:</b> O app geralmente marcará esses arquivos para uma nova tentativa no final da sessão de download.</li><br>\n<li><b>403 Proibido / 401 Não Autorizado (menos comum para publicações públicas):</b><br>\nVocê pode não ter permissão para acessar o conteúdo. Para algum conteúdo pago ou privado, usar a opção 'Usar Cookie' com cookies válidos da sua sessão de navegador pode ajudar. Certifique-se de que seus cookies estão atualizados.</li><br>\n<li><b>404 Não Encontrado:</b><br>\nA URL da publicação ou do arquivo está incorreta, ou o conteúdo foi removido do site. Verifique a URL novamente.</li><br>\n<li><b>'Nenhuma publicação encontrada' / 'Publicação de destino não encontrada':</b><br>\nCertifique-se de que a URL está correta e que o criador/publicação existe. Se estiver usando intervalos de páginas, certifique-se de que são válidos para o criador. Para publicações muito novas, pode haver um pequeno atraso antes que elas apareçam na API.</li><br>\n<li><b>Lentidão Geral / App '(Não Respondendo)':</b><br>\nComo mencionado no Passo 1, se o app parecer travar após o início, especialmente com feeds de criadores grandes ou muitos threads, por favor, dê um tempo. Provavelmente está processando dados em segundo plano. Reduzir a contagem de threads às vezes pode melhorar a capacidade de resposta se isso for frequente.</li>\n</ul>",
"tour_dialog_step8_title":"⑦ Log e Controles Finais",
"tour_dialog_step8_content":"Monitoramento e Controles:\n<ul>\n<li><b>📜 Log de Progresso / Log de Links Extraídos:</b> Mostra mensagens de download detalhadas. Se o modo '🔗 Apenas Links' estiver ativo, esta área exibe os links extraídos.</li><br>\n<li><b>Mostrar Links Externos no Log:</b> Se marcado, um painel de log secundário aparece abaixo do log principal para exibir quaisquer links externos encontrados nas descrições das publicações. <i>(Isso é desativado se o modo '🔗 Apenas Links' ou '📦 Apenas Arquivos' estiver ativo).</i></li><br>\n<li><b>Alternador de Visualização de Log (Botão 👁️ / 🙈):</b><br>\nEste botão (canto superior direito da área de log) alterna a visualização do log principal:\n<ul><li><b>👁️ Log de Progresso (Padrão):</b> Mostra toda a atividade de download, erros e resumos.</li><br>\n<li><b>🙈 Log de Personagens Perdidos:</b> Exibe uma lista de termos-chave dos títulos das publicações que foram pulados devido às suas configurações de 'Filtrar por Personagem(ns)'. Útil para identificar conteúdo que você pode estar perdendo involuntariamente.</li></ul></li><br>\n<li><b>🔄 Reiniciar:</b> Limpa todos os campos de entrada, logs e redefine as configurações temporárias para seus padrões. Só pode ser usado quando nenhum download estiver ativo.</li><br>\n<li><b>⬇️ Iniciar Download / 🔗 Extrair Links / ⏸️ Pausar / ❌ Cancelar:</b> Estes botões controlam o processo. 'Cancelar e Reiniciar UI' interrompe a operação atual e executa uma reinicialização suave da UI, preservando suas entradas de URL e Diretório. 'Pausar/Retomar' permite interromper e continuar temporariamente.</li><br>\n<li>Se alguns arquivos falharem com erros recuperáveis (como 'IncompleteRead'), você pode ser solicitado a tentar novamente no final de uma sessão.</li>\n</ul>\n<br>Você está pronto! Clique em <b>'Concluir'</b> para fechar o tour e começar a usar o downloader.",
"help_guide_dialog_title":"Kemono Downloader - Guia de Recursos",
"help_guide_github_tooltip":"Visitar a página do projeto no GitHub (abre no navegador)",
"help_guide_instagram_tooltip":"Visitar nossa página no Instagram (abre no navegador)",
"help_guide_discord_tooltip":"Visitar nossa comunidade no Discord (abre no navegador)",
"help_guide_step1_title":"① Introdução e Entradas Principais",
"help_guide_step1_content":"<html><head/><body>\n<p>Este guia fornece uma visão geral dos recursos, campos e botões do Kemono Downloader.</p>\n<h3>Área de Entrada Principal (Canto Superior Esquerdo)</h3>\n<ul>\n<li><b>🔗 URL do Criador/Post do Kemono:</b>\n<ul>\n<li>Digite o endereço web completo de uma página de criador (ex: <i>https://kemono.su/patreon/user/12345</i>) ou de uma publicação específica (ex: <i>.../post/98765</i>).</li>\n<li>Suporta URLs do Kemono (kemono.su, kemono.party) e do Coomer (coomer.su, coomer.party).</li>\n</ul>\n</li>\n<li><b>Intervalo de Páginas (Início ao Fim):</b>\n<ul>\n<li>Para URLs de criadores: Especifique um intervalo de páginas para buscar (ex: páginas 2 a 5). Deixe em branco para todas as páginas.</li>\n<li>Desativado para URLs de publicações únicas ou quando o <b>Modo Mangá/Quadrinhos</b> está ativo.</li>\n</ul>\n</li>\n<li><b>📁 Local de Download:</b>\n<ul>\n<li>Clique em <b>'Procurar...'</b> para escolher uma pasta principal em seu computador onde todos os arquivos baixados serão salvos.</li>\n<li>Este campo é obrigatório, a menos que você esteja usando o modo <b>'🔗 Apenas Links'</b>.</li>\n</ul>\n</li>\n<li><b>🎨 Botão de Seleção de Criador (ao lado da Entrada de URL):</b>\n<ul>\n<li>Clique no ícone da paleta (🎨) para abrir o diálogo 'Seleção de Criador'.</li>\n<li>Este diálogo carrega criadores do seu arquivo <code>creators.json</code> (que deve estar no diretório da aplicação).</li>\n<li><b>Dentro do Diálogo:</b>\n<ul>\n<li><b>Barra de Pesquisa:</b> Digite para filtrar a lista de criadores por nome ou serviço.</li>\n<li><b>Lista de Criadores:</b> Exibe criadores do seu <code>creators.json</code>. Criadores que você favoritou (nos dados JSON) aparecem no topo.</li>\n<li><b>Caixas de Seleção:</b> Selecione um ou mais criadores marcando a caixa ao lado de seu nome.</li>\n<li><b>Botão 'Escopo' (ex: 'Escopo: Personagens'):</b> Este botão alterna a organização do download ao iniciar downloads a partir deste pop-up:\n<ul><li><i>Escopo: Personagens:</i> Os downloads serão organizados em pastas com nomes de personagens diretamente em seu 'Local de Download' principal. Obras de diferentes criadores para o mesmo personagem serão agrupadas.</li>\n<li><i>Escopo: Criadores:</i> Os downloads criarão primeiro uma pasta com o nome do criador dentro do seu 'Local de Download' principal. Em seguida, subpastas com nomes de personagens serão criadas dentro da pasta de cada criador.</li></ul>\n</li>\n<li><b>Botão 'Adicionar Selecionados':</b> Clicar aqui pegará os nomes de todos os criadores marcados e os adicionará ao campo de entrada principal '🔗 URL do Criador/Post do Kemono', separados por vírgulas. O diálogo então será fechado.</li>\n</ul>\n</li>\n<li>Este recurso oferece uma maneira rápida de preencher o campo de URL para vários criadores sem ter que digitar ou colar manualmente cada URL.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step2_title":"② Filtrando Downloads",
"help_guide_step2_content":"<html><head/><body>\n<h3>Filtrando Downloads (Painel Esquerdo)</h3>\n<ul>\n<li><b>🎯 Filtrar por Personagem(ns):</b>\n<ul>\n<li>Digite nomes, separados por vírgula (ex: <code>Tifa, Aerith</code>).</li>\n<li><b>Apelidos Agrupados para Pasta Compartilhada (Entradas Separadas no Known.txt):</b> <code>(Vivi, Ulti, Uta)</code>.\n<ul><li>O conteúdo que corresponder a \"Vivi\", \"Ulti\" OU \"Uta\" irá para uma pasta compartilhada chamada \"Vivi Ulti Uta\" (após a limpeza).</li>\n<li>Se esses nomes forem novos, você será solicitado a adicionar \"Vivi\", \"Ulti\" e \"Uta\" como <i>entradas individuais separadas</i> ao <code>Known.txt</code>.</li>\n</ul>\n</li>\n<li><b>Apelidos Agrupados para Pasta Compartilhada (Entrada Única no Known.txt):</b> <code>(Yuffie, Sonon)~</code> (note o til <code>~</code>).\n<ul><li>O conteúdo que corresponder a \"Yuffie\" OU \"Sonon\" irá para uma pasta compartilhada chamada \"Yuffie Sonon\".</li>\n<li>Se novo, \"Yuffie Sonon\" (com os apelidos Yuffie, Sonon) será solicitado para ser adicionado como uma <i>única entrada de grupo</i> ao <code>Known.txt</code>.</li>\n</ul>\n</li>\n<li>Este filtro influencia a nomenclatura de pastas se 'Pastas Separadas por Nome/Título' estiver habilitado.</li>\n</ul>\n</li>\n<li><b>Filtro: Botão [Tipo] (Escopo do Filtro de Personagem):</b> Alterna como o 'Filtrar por Personagem(ns)' se aplica:\n<ul>\n<li><code>Filtro: Arquivos</code>: Verifica nomes de arquivos individuais. Uma publicação é mantida se algum arquivo corresponder; apenas os arquivos correspondentes são baixados. A nomenclatura de pastas usa o personagem do nome do arquivo correspondente.</li>\n<li><code>Filtro: Título</code>: Verifica títulos de publicações. Todos os arquivos de uma publicação correspondente são baixados. A nomenclatura de pastas usa o personagem do título da publicação correspondente.</li>\n<li><code>Filtro: Ambos</code>: Verifica o título da publicação primeiro. Se corresponder, todos os arquivos são baixados. Se não, verifica os nomes dos arquivos, e apenas os arquivos correspondentes são baixados. A nomenclatura de pastas prioriza a correspondência de título, depois a correspondência de arquivo.</li>\n<li><code>Filtro: Comentários (Beta)</code>: Verifica os nomes dos arquivos primeiro. Se um arquivo corresponder, todos os arquivos da publicação são baixados. Se não houver correspondência de arquivo, então verifica os comentários da publicação. Se um comentário corresponder, todos os arquivos são baixados. (Usa mais solicitações de API). A nomenclatura de pastas prioriza a correspondência de arquivo, depois a correspondência de comentário.</li>\n</ul>\n</li>\n<li><b>🗄️ Nome de Pasta Personalizado (Apenas Publicação Única):</b>\n<ul>\n<li>Visível e utilizável apenas ao baixar uma URL de publicação específica E quando 'Pastas Separadas por Nome/Título' está habilitado.</li>\n<li>Permite que você especifique um nome personalizado para a pasta de download dessa única publicação.</li>\n</ul>\n</li>\n<li><b>🚫 Ignorar com Palavras:</b>\n<ul><li>Digite palavras, separadas por vírgula (ex: <code>WIP, rascunho, prévia</code>) para pular determinado conteúdo.</li></ul>\n</li>\n<li><b>Escopo: Botão [Tipo] (Escopo de Palavras a Ignorar):</b> Alterna como o 'Ignorar com Palavras' se aplica:\n<ul>\n<li><code>Escopo: Arquivos</code>: Pula arquivos individuais se seus nomes contiverem alguma dessas palavras.</li>\n<li><code>Escopo: Publicações</code>: Pula publicações inteiras se seus títulos contiverem alguma dessas palavras.</li>\n<li><code>Escopo: Ambos</code>: Aplica ambos (primeiro o título da publicação, depois os arquivos individuais).</li>\n</ul>\n</li>\n<li><b>✂️ Remover Palavras do nome:</b>\n<ul><li>Digite palavras, separadas por vírgula (ex: <code>patreon, [HD]</code>), para remover dos nomes dos arquivos baixados (não diferencia maiúsculas de minúsculas).</li></ul>\n</li>\n<li><b>Filtrar Arquivos (Botões de Rádio):</b> Escolha o que baixar:\n<ul>\n<li><code>Todos</code>: Baixa todos os tipos de arquivos encontrados.</li>\n<li><code>Imagens/GIFs</code>: Apenas formatos de imagem comuns (JPG, PNG, GIF, WEBP, etc.) e GIFs.</li>\n<li><code>Vídeos</code>: Apenas formatos de vídeo comuns (MP4, MKV, WEBM, MOV, etc.).</li>\n<li><code>📦 Apenas Arquivos</code>: Baixa exclusivamente arquivos <b>.zip</b> e <b>.rar</b>. Quando selecionado, as caixas de seleção 'Pular .zip' e 'Pular .rar' são automaticamente desativadas e desmarcadas. 'Mostrar Links Externos' também é desativado.</li>\n<li><code>🎧 Apenas Áudio</code>: Baixa apenas formatos de áudio comuns (MP3, WAV, FLAC, M4A, OGG, etc.). Outras opções específicas de arquivos se comportam como no modo 'Imagens' ou 'Vídeos'.</li>\n<li><code>🔗 Apenas Links</code>: Extrai e exibe links externos das descrições das publicações em vez de baixar arquivos. As opções relacionadas ao download e 'Mostrar Links Externos' são desativadas. O botão principal de download muda para '🔗 Extrair Links'.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step3_title":"③ Opções e Configurações de Download",
"help_guide_step3_content":"<html><head/><body>\n<h3>Opções e Configurações de Download (Painel Esquerdo)</h3>\n<ul>\n<li><b>Pular .zip / Pular .rar:</b> Caixas de seleção para evitar o download desses tipos de arquivos de arquivamento. (Desativadas e ignoradas se o modo de filtro '📦 Apenas Arquivos' for selecionado).</li>\n<li><b>Baixar Apenas Miniaturas:</b> Baixa pequenas imagens de visualização em vez de arquivos em tamanho real (se disponível).</li>\n<li><b>Comprimir Imagens Grandes (para WebP):</b> Se a biblioteca 'Pillow' (PIL) estiver instalada, imagens maiores que 1.5MB serão convertidas para o formato WebP se a versão WebP for significativamente menor.</li>\n<li><b>⚙️ Configurações Avançadas:</b>\n<ul>\n<li><b>Pastas Separadas por Nome/Título:</b> Cria subpastas com base na entrada 'Filtrar por Personagem(ns)' ou nos títulos das publicações. Pode usar a lista <b>Known.txt</b> como fallback para nomes de pastas.</li></ul></li></ul></body></html>",
"help_guide_step4_title":"④ Configurações Avançadas (Parte 1)",
"help_guide_step4_content":"<html><head/><body><h3>⚙️ Configurações Avançadas (Continuação)</h3><ul><ul>\n<li><b>Subpasta por Publicação:</b> Se 'Pastas Separadas' estiver ativado, isso cria uma subpasta adicional para <i>cada publicação individual</i> dentro da pasta principal do personagem/título.</li>\n<li><b>Usar Cookie:</b> Marque esta caixa para usar cookies para solicitações.\n<ul>\n<li><b>Campo de Texto:</b> Digite uma string de cookie diretamente (ex: <code>nome1=valor1; nome2=valor2</code>).</li>\n<li><b>Procurar...:</b> Selecione um arquivo <code>cookies.txt</code> (formato Netscape). O caminho aparecerá no campo de texto.</li>\n<li><b>Precedência:</b> O campo de texto (se preenchido) tem precedência sobre um arquivo procurado. Se 'Usar Cookie' estiver marcado, mas ambos estiverem vazios, ele tentará carregar <code>cookies.txt</code> do diretório da aplicação.</li>\n</ul>\n</li>\n<li><b>Usar Multithreading e Entrada de Threads:</b>\n<ul>\n<li>Habilita operações mais rápidas. O número na entrada 'Threads' significa:\n<ul>\n<li>Para <b>Feeds de Criadores:</b> Número de publicações a serem processadas simultaneamente. Arquivos dentro de cada publicação são baixados sequencialmente por seu trabalhador (a menos que a nomenclatura de mangá 'Baseada na Data' esteja ativada, o que força 1 trabalhador de publicação).</li>\n<li>Para <b>URLs de Publicações Únicas:</b> Número de arquivos a serem baixados simultaneamente dessa única publicação.</li>\n</ul>\n</li>\n<li>Se não estiver marcado, 1 thread é usado. Contagens altas de threads (ex: >40) podem exibir um aviso.</li>\n</ul>\n</li></ul></ul></body></html>",
"help_guide_step5_title":"⑤ Configurações Avançadas (Parte 2) e Ações",
"help_guide_step5_content":"<html><head/><body><h3>⚙️ Configurações Avançadas (Continuação)</h3><ul><ul>\n<li><b>Mostrar Links Externos no Log:</b> Se marcado, um painel de log secundário aparece abaixo do log principal para exibir quaisquer links externos encontrados nas descrições das publicações. (Desativado se o modo '🔗 Apenas Links' ou '📦 Apenas Arquivos' estiver ativo).</li>\n<li><b>📖 Modo Mangá/Quadrinhos (apenas URL de criador):</b> Adaptado para conteúdo sequencial.\n<ul>\n<li>Baixa as publicações da <b>mais antiga para a mais nova</b>.</li>\n<li>A entrada 'Intervalo de Páginas' é desativada, pois todas as publicações são buscadas.</li>\n<li>Um <b>botão de alternância de estilo de nome de arquivo</b> (ex: 'Nome: Título da Publicação') aparece no canto superior direito da área de log quando este modo está ativo para um feed de criador. Clique nele para alternar entre os estilos de nomenclatura:\n<ul>\n<li><code>Nome: Título da Publicação (Padrão)</code>: O primeiro arquivo em uma publicação é nomeado com base no título limpo da publicação (ex: 'Meu Capítulo 1.jpg'). Arquivos subsequentes na *mesma publicação* tentarão manter seus nomes de arquivo originais (ex: 'pagina_02.png', 'arte_bonus.jpg'). Se a publicação tiver apenas um arquivo, ele será nomeado com base no título da publicação. Isso é geralmente recomendado para a maioria dos mangás/quadrinhos.</li>\n<li><code>Nome: Arquivo Original</code>: Todos os arquivos tentam manter seus nomes de arquivo originais.</li>\n<li><code>Nome: Arquivo Original</code>: Todos os arquivos tentam manter seus nomes de arquivo originais. Quando este estilo está ativo, um campo de entrada para um <b>prefixo de nome de arquivo opcional</b> (ex: 'MinhaSérie_') aparecerá ao lado deste botão de estilo. Exemplo: 'MinhaSérie_ArquivoOriginal.jpg'.</li>\n<li><code>Nome: Título+Núm. Global (Título da Publicação + Numeração Global)</code>: Todos os arquivos em todas as publicações na sessão de download atual são nomeados sequencialmente usando o título limpo da publicação como prefixo, seguido por um contador global. Exemplo: Publicação 'Capítulo 1' (2 arquivos) -> 'Capítulo 1 001.jpg', 'Capítulo 1 002.png'. Próxima publicação 'Capítulo 2' (1 arquivo) -> 'Capítulo 2 003.jpg'. O multithreading para processamento de publicações é desativado automaticamente para este estilo.</li>\n<li><code>Nome: Baseado na Data</code>: Os arquivos são nomeados sequencialmente (001.ext, 002.ext, ...) com base na ordem de publicação. Quando este estilo está ativo, um campo de entrada para um <b>prefixo de nome de arquivo opcional</b> (ex: 'MinhaSérie_') aparecerá ao lado deste botão de estilo. Exemplo: 'MinhaSérie_001.jpg'. O multithreading para processamento de publicações é desativado automaticamente para este estilo.</li>\n</ul>\n</li>\n<li>Para obter os melhores resultados com os estilos 'Nome: Título da Publicação', 'Nome: Título+Núm. Global' ou 'Nome: Baseado na Data', use o campo 'Filtrar por Personagem(ns)' com o título do mangá/série para a organização de pastas.</li>\n</ul>\n</li>\n</ul></li></ul>\n<h3>Botões de Ação Principais (Painel Esquerdo)</h3>\n<ul>\n<li><b>⬇️ Iniciar Download / 🔗 Extrair Links:</b> O texto e a função deste botão mudam com base na seleção do botão de rádio 'Filtrar Arquivos'. Ele inicia a operação principal.</li>\n<li><b>⏸️ Pausar Download / ▶️ Retomar Download:</b> Permite que você interrompa temporariamente o processo de download/extração atual e o retome mais tarde. Algumas configurações da UI podem ser alteradas enquanto estiver em pausa.</li>\n<li><b>❌ Cancelar e Reiniciar UI:</b> Interrompe a operação atual e executa uma reinicialização suave da UI. Suas entradas de URL e Diretório de Download são preservadas, mas outras configurações e logs são limpos.</li>\n</ul></body></html>",
"help_guide_step6_title":"⑥ Lista de Shows/Personagens Conhecidos",
"help_guide_step6_content":"<html><head/><body>\n<h3>Gerenciamento da Lista de Shows/Personagens Conhecidos (Canto Inferior Esquerdo)</h3>\n<p>Esta seção ajuda a gerenciar o arquivo <code>Known.txt</code>, que é usado para organização inteligente de pastas quando 'Pastas Separadas por Nome/Título' está habilitado, especialmente como fallback se uma publicação não corresponder à sua entrada ativa de 'Filtrar por Personagem(ns)'.</p>\n<ul>\n<li><b>Abrir Known.txt:</b> Abre o arquivo <code>Known.txt</code> (localizado no diretório da aplicação) em seu editor de texto padrão para edição avançada (como criar apelidos agrupados complexos).</li>\n<li><b>Pesquisar personagens...:</b> Filtra a lista de nomes conhecidos exibida abaixo.</li>\n<li><b>Widget de Lista:</b> Exibe os nomes principais do seu <code>Known.txt</code>. Selecione entradas aqui para excluí-las.</li>\n<li><b>Adicionar novo nome de show/personagem (Campo de Entrada):</b> Digite um nome ou grupo para adicionar.\n<ul>\n<li><b>Nome Simples:</b> ex: <code>Minha Série Incrível</code>. Adiciona como uma única entrada.</li>\n<li><b>Grupo para Entradas Separadas no Known.txt:</b> ex: <code>(Vivi, Ulti, Uta)</code>. Adiciona \"Vivi\", \"Ulti\" e \"Uta\" como três entradas individuais separadas ao <code>Known.txt</code>.</li>\n<li><b>Grupo para Pasta Compartilhada e Entrada Única no Known.txt (Til <code>~</code>):</b> ex: <code>(Personagem A, Pers A)~</code>. Adiciona uma entrada ao <code>Known.txt</code> chamada \"Personagem A Pers A\". \"Personagem A\" e \"Pers A\" se tornam apelidos para esta única pasta/entrada.</li>\n</ul>\n</li>\n<li><b>➕ Botão Adicionar:</b> Adiciona o nome/grupo do campo de entrada acima à lista e ao <code>Known.txt</code>.</li>\n<li><b>⤵️ Botão Adicionar ao Filtro:</b>\n<ul>\n<li>Localizado ao lado do botão '➕ Adicionar' para a lista 'Shows/Personagens Conhecidos'.</li>\n<li>Clicar neste botão abre uma janela pop-up exibindo todos os nomes do seu arquivo <code>Known.txt</code>, cada um com uma caixa de seleção.</li>\n<li>O pop-up inclui uma barra de pesquisa para filtrar rapidamente a lista de nomes.</li>\n<li>Você pode selecionar um ou mais nomes usando as caixas de seleção.</li>\n<li>Clique em 'Adicionar Selecionados' para inserir os nomes escolhidos no campo de entrada 'Filtrar por Personagem(ns)' na janela principal.</li>\n<li>Se um nome selecionado do <code>Known.txt</code> era originalmente um grupo (ex: definido como <code>(Boa, Hancock)</code> no Known.txt), ele será adicionado ao campo de filtro como <code>(Boa, Hancock)~</code>. Nomes simples são adicionados como estão.</li>\n<li>Para conveniência, os botões 'Selecionar Todos' e 'Desmarcar Todos' estão disponíveis no pop-up.</li>\n<li>Clique em 'Cancelar' para fechar o pop-up sem nenhuma alteração.</li>\n</ul>\n</li>\n<li><b>🗑️ Botão Excluir Selecionados:</b> Exclui os nomes selecionados da lista e do <code>Known.txt</code>.</li>\n<li><b>❓ Botão (este mesmo!):</b> Exibe este guia de ajuda abrangente.</li>\n</ul></body></html>",
"help_guide_step7_title":"⑦ Área de Log e Controles",
"help_guide_step7_content":"<html><head/><body>\n<h3>Área de Log e Controles (Painel Direito)</h3>\n<ul>\n<li><b>📜 Log de Progresso / Log de Links Extraídos (Rótulo):</b> Título da área de log principal; muda se o modo '🔗 Apenas Links' estiver ativo.</li>\n<li><b>Pesquisar Links... / 🔍 Botão (Pesquisa de Links):</b>\n<ul><li>Visível apenas quando o modo '� Apenas Links' está ativo. Permite filtrar em tempo real os links extraídos exibidos no log principal por texto, URL ou plataforma.</li></ul>\n</li>\n<li><b>Nome: Botão [Estilo] (Estilo de Nome de Arquivo de Mangá):</b>\n<ul><li>Visível apenas quando o <b>Modo Mangá/Quadrinhos</b> está ativo para um feed de criador e não no modo 'Apenas Links' ou 'Apenas Arquivos'.</li>\n<li>Alterna entre os estilos de nome de arquivo: <code>Título da Publicação</code>, <code>Arquivo Original</code>, <code>Baseado na Data</code>. (Consulte a seção Modo Mangá/Quadrinhos para mais detalhes).</li>\n<li>Quando o estilo 'Arquivo Original' ou 'Baseado na Data' está ativo, um campo de entrada para um <b>prefixo de nome de arquivo opcional</b> aparecerá ao lado deste botão.</li>\n</ul>\n</li>\n<li><b>Multiparte: Botão [LIGADO/DESLIGADO]:</b>\n<ul><li>Alterna downloads multissegmento para arquivos grandes individuais.\n<ul><li><b>LIGADO:</b> Pode acelerar o download de arquivos grandes (ex: vídeos), mas pode aumentar a instabilidade da UI ou o spam de log com muitos arquivos pequenos. Um aviso aparece ao habilitar. Se um download multiparte falhar, ele tenta novamente como um único fluxo.</li>\n<li><b>DESLIGADO (Padrão):</b> Os arquivos são baixados em um único fluxo.</li>\n</ul>\n<li>Desativado se o modo '🔗 Apenas Links' ou '📦 Apenas Arquivos' estiver ativo.</li>\n</ul>\n</li>\n<li><b>👁️ / 🙈 Botão (Alternador de Visualização de Log):</b> Alterna a visualização do log principal:\n<ul>\n<li><b>👁️ Log de Progresso (Padrão):</b> Mostra toda a atividade de download, erros e resumos.</li>\n<li><b>🙈 Log de Personagens Perdidos:</b> Exibe uma lista de termos-chave dos títulos/conteúdos das publicações que foram pulados devido às suas configurações de 'Filtrar por Personagem(ns)'. Útil para identificar conteúdo que você pode estar perdendo involuntariamente.</li>\n</ul>\n</li>\n<li><b>🔄 Botão Reiniciar:</b> Limpa todos os campos de entrada, logs e redefine as configurações temporárias para seus padrões. Só pode ser usado quando nenhum download estiver ativo.</li>\n<li><b>Saída do Log Principal (Área de Texto):</b> Exibe mensagens de progresso detalhadas, erros e resumos. Se o modo '🔗 Apenas Links' estiver ativo, esta área exibe os links extraídos.</li>\n<li><b>Saída do Log de Personagens Perdidos (Área de Texto):</b> (Visível através do alternador 👁️ / 🙈) Exibe as publicações/arquivos pulados devido aos filtros de personagem.</li>\n<li><b>Saída do Log Externo (Área de Texto):</b> Aparece abaixo do log principal se 'Mostrar Links Externos no Log' estiver marcado. Exibe links externos encontrados nas descrições das publicações.</li>\n<li><b>Botão Exportar Links:</b>\n<ul><li>Visível e habilitado apenas quando o modo '🔗 Apenas Links' está ativo e os links foram extraídos.</li>\n<li>Permite que você salve todos os links extraídos em um arquivo <code>.txt</code>.</li>\n</ul>\n</li>\n<li><b>Progresso: Rótulo [Status]:</b> Mostra o progresso geral do processo de download ou extração de links (ex: publicações processadas).</li>\n<li><b>Rótulo de Progresso do Arquivo:</b> Mostra o progresso dos downloads de arquivos individuais, incluindo velocidade e tamanho, ou o status do download multiparte.</li>\n</ul></body></html>",
"help_guide_step8_title":"⑧ Modo Favoritos e Recursos Futuros",
"help_guide_step8_content":"<html><head/><body>\n<h3>Modo Favoritos (Baixando de seus favoritos do Kemono.su)</h3>\n<p>Este modo permite que você baixe conteúdo diretamente de artistas que você favoritou no Kemono.su.</p>\n<ul>\n<li><b>⭐ Como Habilitar:</b>\n<ul>\n<li>Marque a caixa de seleção <b>'⭐ Modo Favoritos'</b>, localizada ao lado do botão de rádio '🔗 Apenas Links'.</li>\n</ul>\n</li>\n<li><b>Mudanças na UI no Modo Favoritos:</b>\n<ul>\n<li>A área de entrada '🔗 URL do Criador/Post do Kemono' é substituída por uma mensagem indicando que o Modo Favoritos está ativo.</li>\n<li>Os botões padrão 'Iniciar Download', 'Pausar', 'Cancelar' são substituídos por:\n<ul>\n<li>Botão <b>'🖼️ Artistas Favoritos'</b></li>\n<li>Botão <b>'📄 Publicações Favoritas'</b></li>\n</ul>\n</li>\n<li>A opção '🍪 Usar Cookie' é automaticamente habilitada e bloqueada, pois os cookies são necessários para buscar seus favoritos.</li>\n</ul>\n</li>\n<li><b>🖼️ Botão Artistas Favoritos:</b>\n<ul>\n<li>Clicar aqui abre um diálogo que lista todos os artistas que você favoritou no Kemono.su.</li>\n<li>Você pode selecionar um ou mais artistas desta lista para baixar seu conteúdo.</li>\n</ul>\n</li>\n<li><b>📄 Botão Publicações Favoritas (Recurso Futuro):</b>\n<ul>\n<li>O download de <i>publicações</i> específicas favoritadas (especialmente em uma ordem sequencial tipo mangá se fizerem parte de uma série) é um recurso atualmente em desenvolvimento.</li>\n<li>A melhor maneira de lidar com publicações favoritadas, especialmente para leitura sequencial como mangá, ainda está sendo explorada.</li>\n<li>Se você tiver ideias ou casos de uso específicos sobre como gostaria de baixar e organizar publicações favoritadas (ex: 'estilo mangá' a partir de favoritos), considere abrir um issue ou participar da discussão na página do GitHub do projeto. Sua contribuição é valiosa!</li>\n</ul>\n</li>\n<li><b>Escopo de Download de Favoritos (botão):</b>\n<ul>\n<li>Este botão (ao lado de 'Publicações Favoritas') controla onde o conteúdo de artistas favoritos selecionados é baixado:\n<ul>\n<li><b><i>Escopo: Local Selecionado:</i></b> Todos os artistas selecionados são baixados para o 'Local de Download' principal que você definiu na UI. Os filtros se aplicam globalmente a todo o conteúdo.</li>\n<li><b><i>Escopo: Pastas de Artistas:</i></b> Para cada artista selecionado, uma subpasta (com o nome do artista) é criada automaticamente dentro do seu 'Local de Download' principal. O conteúdo desse artista vai para sua pasta específica. Os filtros se aplicam dentro da pasta dedicada de cada artista.</li>\n</ul>\n</li>\n</ul>\n</li>\n<li><b>Filtros no Modo Favoritos:</b>\n<ul>\n<li>As opções '🎯 Filtrar por Personagem(ns)', '🚫 Ignorar com Palavras' e 'Filtrar Arquivos' que você definiu na UI ainda se aplicarão ao conteúdo baixado de seus artistas favoritos selecionados.</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step9_title":"⑨ Arquivos Chave e Tour",
"help_guide_step9_content":"<html><head/><body>\n<h3>Arquivos Chave Usados pela Aplicação</h3>\n<ul>\n<li><b><code>Known.txt</code>:</b>\n<ul>\n<li>Localizado no diretório da aplicação (onde está o <code>.exe</code> ou <code>main.py</code>).</li>\n<li>Armazena sua lista de shows, personagens ou títulos de séries conhecidos para organização automática de pastas quando 'Pastas Separadas por Nome/Título' está habilitado.</li>\n<li><b>Formato:</b>\n<ul>\n<li>Cada linha é uma entrada.</li>\n<li><b>Nome Simples:</b> ex: <code>Minha Série Incrível</code>. O conteúdo que corresponder a isso irá para uma pasta chamada \"Minha Série Incrível\".</li>\n<li><b>Apelidos Agrupados:</b> ex: <code>(Personagem A, Pers A, Nome Alt A)</code>. O conteúdo que corresponder a \"Personagem A\", \"Pers A\" OU \"Nome Alt A\" irá TODO para uma única pasta chamada \"Personagem A Pers A Nome Alt A\" (após a limpeza). Todos os termos entre parênteses se tornam apelidos para essa pasta.</li>\n</ul>\n</li>\n<li><b>Uso:</b> Serve como fallback para a nomenclatura de pastas se uma publicação não corresponder à sua entrada ativa de 'Filtrar por Personagem(ns)'. Você pode gerenciar entradas simples através da UI ou editar o arquivo diretamente para apelidos complexos. O app o recarrega na inicialização ou no próximo uso.</li>\n</ul>\n</li>\n<li><b><code>cookies.txt</code> (Opcional):</b>\n<ul>\n<li>Se você usar o recurso 'Usar Cookie' e não fornecer uma string de cookie direta ou procurar um arquivo específico, a aplicação procurará por um arquivo chamado <code>cookies.txt</code> em seu diretório.</li>\n<li><b>Formato:</b> Deve estar no formato de arquivo de cookie Netscape.</li>\n<li><b>Uso:</b> Permite que o downloader use a sessão de login do seu navegador para acessar conteúdo que pode estar por trás de um login no Kemono/Coomer.</li>\n</ul>\n</li>\n</ul>\n<h3>Tour para o Primeiro Usuário</h3>\n<ul>\n<li>Na primeira inicialização (ou se reiniciado), um diálogo de tour de boas-vindas aparece, guiando você pelas principais funcionalidades. Você pode pulá-lo ou escolher 'Não mostrar este tour novamente'.</li>\n</ul>\n<p><em>Muitos elementos da UI também têm dicas de ferramentas que aparecem quando você passa o mouse sobre eles, fornecendo dicas rápidas.</em></p>\n</body></html>"
})

translations ["zh_TW"]={}
translations ["zh_TW"].update ({
"settings_dialog_title":"設定",
"language_label":"語言：",
"lang_english":"英文 (English)",
"lang_japanese":"日文 (日本語)",
"theme_toggle_light":"切換到淺色模式",
"theme_toggle_dark":"切換到深色模式",
"theme_tooltip_light":"將應用程式外觀切換為淺色。",
"theme_tooltip_dark":"將應用程式外觀切換為深色。",
"ok_button":"確定",
"appearance_group_title":"外觀",
"language_group_title":"語言設定",
"creator_post_url_label":"🔗 Kemono 創作者/貼文網址：",
"download_location_label":"📁 下載位置：",
"filter_by_character_label":"🎯 按角色篩選（以逗號分隔）：",
"skip_with_words_label":"🚫 使用關鍵字跳過（以逗號分隔）：",
"remove_words_from_name_label":"✂️ 從名稱中移除單字：",
"filter_all_radio":"全部",
"filter_images_radio":"圖片/GIF",
"filter_videos_radio":"影片",
"filter_archives_radio":"📦 僅限壓縮檔",
"filter_links_radio":"� 僅限連結",
"filter_audio_radio":"🎧 僅限音訊",
"favorite_mode_checkbox_label":"⭐ 最愛模式",
"browse_button_text":"瀏覽...",
"char_filter_scope_files_text":"篩選：檔案",
"char_filter_scope_files_tooltip":"目前範圍：檔案\n\n按檔名篩選個別檔案。如果任何檔案符合條件，則保留該貼文。\n僅下載該貼文中符合條件的檔案。\n範例：篩選「Tifa」。檔案「Tifa_artwork.jpg」符合條件並被下載。\n資料夾命名：使用符合條件的檔案名稱中的角色。\n\n點擊切換至：兩者",
"char_filter_scope_title_text":"篩選：標題",
"char_filter_scope_title_tooltip":"目前範圍：標題\n\n按標題篩選整個貼文。符合條件的貼文中的所有檔案都將被下載。\n範例：篩選「Aerith」。標題為「Aerith's Garden」的貼文符合條件；其所有檔案都將被下載。\n資料夾命名：使用符合條件的貼文標題中的角色。\n\n點擊切換至：檔案",
"char_filter_scope_both_text":"篩選：兩者",
"char_filter_scope_both_tooltip":"目前範圍：兩者 (標題優先，然後是檔案)\n\n1. 檢查貼文標題：如果符合，則下載該貼文的所有檔案。\n2. 如果標題不符合，則檢查檔名：如果任何檔案符合，則僅下載該檔案。\n範例：篩選「Cloud」。\n - 貼文「Cloud Strife」(標題符合) -> 下載所有檔案。\n - 貼文「Motorcycle Chase」中包含「Cloud_fenrir.jpg」(檔案符合) -> 僅下載「Cloud_fenrir.jpg」。\n資料夾命名：優先使用標題符合項，其次是檔案符合項。\n\n點擊切換至：留言",
"char_filter_scope_comments_text":"篩選：留言 (Beta)",
"char_filter_scope_comments_tooltip":"目前範圍：留言 (Beta - 檔案優先，留言備用)\n\n1. 檢查檔名：如果貼文中的任何檔案符合篩選條件，則下載整個貼文。不會對此篩選詞檢查留言。\n2. 如果沒有檔案符合，則檢查貼文留言：如果留言符合，則下載整個貼文。\n範例：篩選「Barret」。\n - 貼文 A：檔案「Barret_gunarm.jpg」、「other.png」。檔案「Barret_gunarm.jpg」符合。下載貼文 A 的所有檔案。不會檢查留言中是否有「Barret」。\n - 貼文 B：檔案「dyne.jpg」、「weapon.gif」。留言：「...一張 Barret Wallace 的素描...」。沒有檔案符合「Barret」。留言符合。下載貼文 B 的所有檔案。\n資料夾命名：優先使用檔案符合項的角色，其次是留言符合項。\n\n點擊切換至：標題",
"char_filter_scope_unknown_text":"篩選：未知",
"char_filter_scope_unknown_tooltip":"目前範圍：未知\n\n角色篩選範圍處於未知狀態。請切換或重設。\n\n點擊切換至：標題",
"skip_words_input_tooltip":"輸入單字（以逗號分隔）以跳過下載某些內容（例如：WIP、草稿、預覽）。\n\n此輸入旁邊的「範圍：[類型]」按鈕可切換此篩選器的應用方式：\n- 範圍：檔案：如果檔案名稱包含任何這些單字，則跳過個別檔案。\n- 範圍：貼文：如果貼文標題包含任何這些單字，則跳過整個貼文。\n- 範圍：兩者：同時應用兩者（先檢查貼文標題，如果貼文標題沒問題，再檢查個別檔案）。",
"remove_words_input_tooltip":"輸入單字（以逗號分隔）以從下載的檔案名稱中移除（不區分大小寫）。\n用於清理常見的前綴/後綴。\n範例：patreon, kemono, [HD], _final",
"skip_scope_files_text":"範圍：檔案",
"skip_scope_files_tooltip":"目前跳過範圍：檔案\n\n如果個別檔案的名稱包含任何「要跳過的單字」，則跳過這些檔案。\n範例：跳過單字「WIP, draft」。\n- 檔案「art_WIP.jpg」-> 跳過。\n- 檔案「art_final.png」-> 下載（如果滿足其他條件）。\n\n貼文仍會處理其他未跳過的檔案。\n點擊切換至：兩者",
"skip_scope_posts_text":"範圍：貼文",
"skip_scope_posts_tooltip":"目前跳過範圍：貼文\n\n如果貼文標題包含任何「要跳過的單字」，則跳過整個貼文。\n所有被跳過貼文中的檔案都將被忽略。\n範例：跳過單字「preview, announcement」。\n- 貼文「Exciting Announcement!」-> 跳過。\n- 貼文「Finished Artwork」-> 處理（如果滿足其他條件）。\n\n點擊切換至：檔案",
"skip_scope_both_text":"範圍：兩者",
"skip_scope_both_tooltip":"目前跳過範圍：兩者 (貼文優先，然後是檔案)\n\n1. 檢查貼文標題：如果標題包含要跳過的單字，則跳過整個貼文。\n2. 如果貼文標題沒問題，則檢查個別檔名：如果檔名包含要跳過的單字，則僅跳過該檔案。\n範例：跳過單字「WIP, draft」。\n- 貼文「Drafts and WIPs」(標題符合) -> 跳過整個貼文。\n- 貼文「Art Update」(標題沒問題) 中的檔案：\n - 「character_WIP.jpg」(檔案符合) -> 跳過。\n - 「scene_final.png」(檔案沒問題) -> 下載。\n\n點擊切換至：貼文",
"skip_scope_unknown_text":"範圍：未知",
"skip_scope_unknown_tooltip":"要跳過的單字範圍處於未知狀態。請切換或重設。\n\n點擊切換至：貼文",
"language_change_title":"語言已變更",
"language_change_message":"語言已變更。需要重新啟動以使所有變更完全生效。",
"language_change_informative":"您要立即重新啟動應用程式嗎？",
"restart_now_button":"立即重新啟動",
"skip_zip_checkbox_label":"跳過 .zip",
"skip_rar_checkbox_label":"跳過 .rar",
"download_thumbnails_checkbox_label":"僅下載縮圖",
"scan_content_images_checkbox_label":"掃描內容中的圖片",
"compress_images_checkbox_label":"壓縮為 WebP",
"separate_folders_checkbox_label":"按名稱/標題分開資料夾",
"subfolder_per_post_checkbox_label":"每個貼文一個子資料夾",
"use_cookie_checkbox_label":"使用 Cookie",
"use_multithreading_checkbox_base_label":"使用多執行緒",
"show_external_links_checkbox_label":"在日誌中顯示外部連結",
"manga_comic_mode_checkbox_label":"漫畫/漫畫模式",
"threads_label":"執行緒：",
"start_download_button_text":"⬇️ 開始下載",
"start_download_button_tooltip":"點擊以使用目前設定開始下載或提取連結。",
"extract_links_button_text":"🔗 提取連結",
"pause_download_button_text":"⏸️ 暫停下載",
"pause_download_button_tooltip":"點擊以暫停進行中的下載。",
"resume_download_button_text":"▶️ 繼續下載",
"resume_download_button_tooltip":"點擊以繼續下載。",
"cancel_button_text":"❌ 取消並重設介面",
"cancel_button_tooltip":"點擊以取消進行中的下載/提取過程並重設介面欄位（保留網址和目錄）。",
"error_button_text":"錯誤",
"error_button_tooltip":"查看因錯誤而跳過的檔案，並可選擇重試。",
"cancel_retry_button_text":"❌ 取消重試",
"known_chars_label_text":"🎭 已知節目/角色（用於資料夾命名）：",
"open_known_txt_button_text":"開啟 Known.txt",
"known_chars_list_tooltip":"此列表包含在啟用「分開資料夾」且未提供或未符合特定「按角色篩選」時用於自動建立資料夾的名稱。\n新增您經常下載的系列、遊戲或角色名稱。",
"open_known_txt_button_tooltip":"在您的預設文字編輯器中開啟「Known.txt」檔案。\n該檔案位於應用程式目錄中。",
"add_char_button_text":"➕ 新增",
"add_char_button_tooltip":"將輸入欄位中的名稱新增至「已知節目/角色」列表。",
"add_to_filter_button_text":"⤵️ 新增至篩選器",
"add_to_filter_button_tooltip":"從「已知節目/角色」列表中選取名稱，以新增至上方的「按角色篩選」欄位。",
"delete_char_button_text":"🗑️ 刪除所選",
"delete_char_button_tooltip":"從「已知節目/角色」列表中刪除所選名稱。",
"progress_log_label_text":"📜 進度日誌：",
"radio_all_tooltip":"下載貼文中找到的所有檔案類型。",
"radio_images_tooltip":"僅下載常見的圖片格式（JPG、PNG、GIF、WEBP 等）。",
"radio_videos_tooltip":"僅下載常見的影片格式（MP4、MKV、WEBM、MOV 等）。",
"radio_only_archives_tooltip":"專門下載 .zip 和 .rar 檔案。其他特定檔案選項將被停用。",
"radio_only_audio_tooltip":"僅下載常見的音訊格式（MP3、WAV、FLAC 等）。",
"radio_only_links_tooltip":"從貼文描述中提取並顯示外部連結，而不是下載檔案。\n與下載相關的選項將被停用。",
"favorite_mode_checkbox_tooltip":"啟用最愛模式以瀏覽已儲存的藝術家/貼文。\n這將用最愛選擇按鈕取代網址輸入。",
"skip_zip_checkbox_tooltip":"如果勾選，將不會下載 .zip 壓縮檔。\n（如果選擇「僅限壓縮檔」則停用）。",
"skip_rar_checkbox_tooltip":"如果勾選，將不會下載 .rar 壓縮檔。\n（如果選擇「僅限壓縮檔」則停用）。",
"download_thumbnails_checkbox_tooltip":"下載 API 中的小預覽圖，而不是完整大小的檔案（如果可用）。\n如果同時勾選「掃描貼文內容中的圖片網址」，此模式將*僅*下載透過內容掃描找到的圖片（忽略 API 縮圖）。",
"scan_content_images_checkbox_tooltip":"如果勾選，下載器將掃描貼文的 HTML 內容以尋找圖片網址（來自 <img> 標籤或直接連結）。\n這包括將 <img> 標籤中的相對路徑解析為完整網址。\n<img> 標籤中的相對路徑（例如：/data/image.jpg）將被解析為完整網址。\n適用於圖片位於貼文描述中但不在 API 檔案/附件列表中的情況。",
"compress_images_checkbox_tooltip":"將大於 1.5MB 的圖片壓縮為 WebP 格式（需要 Pillow）。",
"use_subfolders_checkbox_tooltip":"根據「按角色篩選」輸入或貼文標題建立子資料夾。\n如果沒有特定的篩選條件符合，則使用「已知節目/角色」列表作為資料夾名稱的備用選項。\n為單一貼文啟用「按角色篩選」和「自訂資料夾名稱」輸入。",
"use_subfolder_per_post_checkbox_tooltip":"為每個貼文建立一個子資料夾。如果同時啟用「分開資料夾」，它將位於角色/標題資料夾內。",
"use_cookie_checkbox_tooltip":"如果勾選，將嘗試使用應用程式目錄中「cookies.txt」（Netscape 格式）的 cookie 進行請求。\n用於存取需要登入 Kemono/Coomer 的內容。",
"cookie_text_input_tooltip":"直接輸入您的 cookie 字串。\n如果勾選「使用 Cookie」且「cookies.txt」找不到或此欄位不為空，則將使用此字串。\n格式取決於後端如何解析它（例如：「name1=value1; name2=value2」）。",
"use_multithreading_checkbox_tooltip":"啟用並行操作。有關詳細資訊，請參閱「執行緒」輸入。",
"thread_count_input_tooltip":"並行操作的數量。\n- 單一貼文：並行檔案下載（建議 1-10）。\n- 創作者動態網址：同時處理的貼文數量（建議 1-200）。\n 每個貼文中的檔案由其工作執行緒逐一下載。\n如果未勾選「使用多執行緒」，則使用 1 個執行緒。",
"external_links_checkbox_tooltip":"如果勾選，主日誌下方會出現一個次要日誌面板，用於顯示在貼文描述中找到的外部連結。\n（如果「僅限連結」或「僅限壓縮檔」模式處於活動狀態，則停用）。",
"manga_mode_checkbox_tooltip":"從最舊到最新下載貼文，並根據貼文標題重新命名檔案（僅適用於創作者動態）。",
"multipart_on_button_text":"多部分：開啟",
"multipart_on_button_tooltip":"多部分下載：開啟\n\n啟用同時下載大型檔案的多個部分。\n- 可以加快單個大型檔案（例如影片）的下載速度。\n- 可能會增加 CPU/網路使用率。\n- 對於包含許多小檔案的動態，這可能無法提供速度優勢，並可能使介面/日誌變得混亂。\n- 如果多部分下載失敗，它會以單一串流重試。\n\n點擊以關閉。",
"multipart_off_button_text":"多部分：關閉",
"multipart_off_button_tooltip":"多部分下載：關閉\n\n所有檔案都使用單一串流下載。\n- 穩定且在大多數情況下運作良好，特別是對於許多較小的檔案。\n- 大型檔案按順序下載。\n\n點擊以開啟（請參閱警告）。",
"reset_button_text":"🔄 重設",
"reset_button_tooltip":"將所有輸入和日誌重設為預設狀態（僅在閒置時）。",
"progress_idle_text":"進度：閒置",
"missed_character_log_label_text":"🚫 遺漏的角色日誌：",
"creator_popup_title":"創作者選擇",
"creator_popup_search_placeholder":"按名稱、服務搜尋或貼上創作者網址...",
"creator_popup_add_selected_button":"新增所選",
"creator_popup_scope_characters_button":"範圍：角色",
"creator_popup_scope_creators_button":"範圍：創作者",
"favorite_artists_button_text":"🖼️ 最愛的藝術家",
"favorite_artists_button_tooltip":"瀏覽並從您在 Kemono.su/Coomer.su 上最愛的藝術家下載。",
"favorite_posts_button_text":"📄 最愛的貼文",
"favorite_posts_button_tooltip":"瀏覽並從您在 Kemono.su/Coomer.su 上最愛的貼文下載。",
"favorite_scope_selected_location_text":"範圍：所選位置",
"favorite_scope_selected_location_tooltip":"目前最愛下載範圍：所選位置\n\n所有選定的最愛藝術家/貼文將下載到介面中指定的主要「下載位置」。\n篩選器（角色、跳過單字、檔案類型）將全域應用於所有內容。\n\n點擊以變更為：藝術家資料夾",
"favorite_scope_artist_folders_text":"範圍：藝術家資料夾",
"favorite_scope_artist_folders_tooltip":"目前最愛下載範圍：藝術家資料夾\n\n對於每個選定的最愛藝術家/貼文，將在主要「下載位置」內建立一個新的子資料夾（以藝術家姓名命名）。\n該藝術家/貼文的內容將下載到其特定的子資料夾中。\n篩選器（角色、跳過單字、檔案類型）將在每個藝術家的資料夾*內*應用。\n\n點擊以變更為：所選位置",
"favorite_scope_unknown_text":"範圍：未知",
"favorite_scope_unknown_tooltip":"最愛下載範圍未知。請點擊切換。",
"manga_style_post_title_text":"命名：貼文標題",
"manga_style_original_file_text":"命名：原始檔案",
"manga_style_date_based_text":"命名：基於日期",
"manga_style_title_global_num_text":"命名：標題+全域編號",
"manga_style_unknown_text":"命名：未知樣式",
"fav_artists_dialog_title":"最愛的藝術家",
"fav_artists_loading_status":"正在載入最愛的藝術家...",
"fav_artists_search_placeholder":"搜尋藝術家...",
"fav_artists_select_all_button":"全選",
"fav_artists_deselect_all_button":"取消全選",
"fav_artists_download_selected_button":"下載所選",
"fav_artists_cancel_button":"取消",
"fav_artists_loading_from_source_status":"⏳ 正在從 {source_name} 載入最愛...",
"fav_artists_found_status":"總共找到 {count} 位最愛的藝術家。",
"fav_artists_none_found_status":"在 Kemono.su 或 Coomer.su 上找不到任何最愛的藝術家。",
"fav_artists_failed_status":"擷取最愛失敗。",
"fav_artists_cookies_required_status":"錯誤：已啟用 Cookie，但無法為任何來源載入。",
"fav_artists_no_favorites_after_processing":"處理後找不到任何最愛的藝術家。",
"fav_artists_no_selection_title":"未選取",
"fav_artists_no_selection_message":"請至少選擇一位藝術家進行下載。",
"fav_posts_dialog_title":"最愛的貼文",
"fav_posts_loading_status":"正在載入最愛的貼文...",
"fav_posts_search_placeholder":"搜尋貼文（標題、創作者、ID、服務）...",
"fav_posts_select_all_button":"全選",
"fav_posts_deselect_all_button":"取消全選",
"fav_posts_download_selected_button":"下載所選",
"fav_posts_cancel_button":"取消",
"fav_posts_cookies_required_error":"錯誤：最愛的貼文需要 Cookie，但無法載入。",
"fav_posts_auth_failed_title":"驗證失敗（貼文）",
"fav_posts_auth_failed_message":"由於授權錯誤，無法擷取最愛{domain_specific_part}：\n\n{error_message}\n\n這通常表示您的 cookie 遺失、無效或已過期。請檢查您的 cookie 設定。",
"fav_posts_fetch_error_title":"擷取錯誤",
"fav_posts_fetch_error_message":"從 {domain} 擷取最愛時發生錯誤{error_message_part}",
"fav_posts_no_posts_found_status":"找不到任何最愛的貼文。",
"fav_posts_found_status":"找到 {count} 個最愛的貼文。",
"fav_posts_display_error_status":"顯示貼文時發生錯誤：{error}",
"fav_posts_ui_error_title":"介面錯誤",
"fav_posts_ui_error_message":"無法顯示最愛的貼文：{error}",
"fav_posts_auth_failed_message_generic":"由於授權錯誤，無法擷取最愛{domain_specific_part}。這通常表示您的 cookie 遺失、無效或已過期。請檢查您的 cookie 設定。",
"key_fetching_fav_post_list_init":"正在擷取最愛的貼文列表...",
"key_fetching_from_source_kemono_su":"正在從 Kemono.su 擷取最愛...",
"key_fetching_from_source_coomer_su":"正在從 Coomer.su 擷取最愛...",
"fav_posts_fetch_cancelled_status":"最愛的貼文擷取已取消。",
"known_names_filter_dialog_title":"將已知名稱新增至篩選器",
"known_names_filter_search_placeholder":"搜尋名稱...",
"known_names_filter_select_all_button":"全選",
"known_names_filter_deselect_all_button":"取消全選",
"known_names_filter_add_selected_button":"新增所選",
"error_files_dialog_title":"因錯誤而跳過的檔案",
"error_files_no_errors_label":"在上次工作階段或重試後，沒有檔案因錯誤而被記錄為已跳過。",
"error_files_found_label":"由於下載錯誤，以下 {count} 個檔案被跳過：",
"error_files_select_all_button":"全選",
"error_files_retry_selected_button":"重試所選",
"error_files_export_urls_button":"將網址匯出至 .txt",
"error_files_no_selection_retry_message":"請至少選擇一個檔案進行重試。",
"error_files_no_errors_export_title":"沒有錯誤",
"error_files_no_errors_export_message":"沒有錯誤檔案網址可匯出。",
"error_files_no_urls_found_export_title":"找不到網址",
"error_files_no_urls_found_export_message":"無法從錯誤檔案列表中提取任何網址進行匯出。",
"error_files_save_dialog_title":"儲存錯誤檔案網址",
"error_files_export_success_title":"匯出成功",
"error_files_export_success_message":"{count} 個項目已成功匯出至：\n{filepath}",
"error_files_export_error_title":"匯出錯誤",
"error_files_export_error_message":"無法匯出檔案連結：{error}",
"export_options_dialog_title":"匯出選項",
"export_options_description_label":"選擇匯出錯誤檔案連結的格式：",
"export_options_radio_link_only":"每行一個連結（僅網址）",
"export_options_radio_link_only_tooltip":"僅匯出每個失敗檔案的直接下載網址，每行一個網址。",
"export_options_radio_with_details":"匯出詳細資訊（網址 [貼文、檔案資訊]）",
"export_options_radio_with_details_tooltip":"匯出網址，後面跟著貼文標題、貼文 ID 和原始檔名等詳細資訊（置於方括號中）。",
"export_options_export_button":"匯出",
"no_errors_logged_title":"未記錄任何錯誤",
"no_errors_logged_message":"在上次工作階段或重試後，沒有檔案因錯誤而被記錄為已跳過。",
"progress_initializing_text":"進度：正在初始化...",
"progress_posts_text":"進度：{processed_posts} / {total_posts} 篇貼文 ({progress_percent:.1f}%)",
"progress_processing_post_text":"進度：正在處理第 {processed_posts} 篇貼文...",
"progress_starting_text":"進度：正在開始...",
"downloading_file_known_size_text":"正在下載 '{filename}' ({downloaded_mb:.1f}MB / {total_mb:.1f}MB)",
"downloading_file_unknown_size_text":"正在下載 '{filename}' ({downloaded_mb:.1f}MB)",
"downloading_multipart_text":"下載 '{filename}...': {downloaded_mb:.1f}/{total_mb:.1f} MB ({parts} 個部分 @ {speed:.2f} MB/s)",
"downloading_multipart_initializing_text":"檔案：{filename} - 正在初始化各部分...",
"status_completed":"已完成",
"status_cancelled_by_user":"使用者已取消",
"files_downloaded_label":"已下載",
"files_skipped_label":"已跳過",
"retry_finished_text":"重試完成",
"succeeded_text":"成功",
"failed_text":"失敗",
"ready_for_new_task_text":"準備好執行新任務。",
"fav_mode_active_label_text":"⭐ 最愛模式已啟用。請在選擇您最愛的藝術家/貼文之前選擇下方的篩選器。請在下方選擇一個操作。",
"export_links_button_text":"匯出連結",
"download_extracted_links_button_text":"下載",
"download_selected_button_text":"下載所選",
"link_input_placeholder_text":"例如：https://kemono.su/patreon/user/12345 或 .../post/98765",
"link_input_tooltip_text":"輸入 Kemono/Coomer 創作者頁面或特定貼文的完整網址。\n範例（創作者）：https://kemono.su/patreon/user/12345\n範例（貼文）：https://kemono.su/patreon/user/12345/post/98765",
"dir_input_placeholder_text":"選擇下載儲存的資料夾",
"dir_input_tooltip_text":"輸入或瀏覽要儲存所有下載內容的主要資料夾。\n除非選擇「僅限連結」模式，否則此欄位為必填。",
"character_input_placeholder_text":"例如：Tifa, Aerith, (Cloud, Zack)",
"custom_folder_input_placeholder_text":"可選：將此貼文儲存到特定資料夾",
"custom_folder_input_tooltip_text":"如果您正在下載單一貼文網址且已啟用「按名稱/標題分開資料夾」，\n您可以在此處為該貼文的下載資料夾輸入自訂名稱。\n範例：我最愛的場景",
"skip_words_input_placeholder_text":"例如：WM, WIP, draft, preview",
"remove_from_filename_input_placeholder_text":"例如：patreon, HD",
"cookie_text_input_placeholder_no_file_selected_text":"Cookie 字串（如果未選擇 cookies.txt）",
"cookie_text_input_placeholder_with_file_selected_text":"正在使用所選的 cookie 檔案（請參閱瀏覽...）",
"character_search_input_placeholder_text":"搜尋角色...",
"character_search_input_tooltip_text":"在此處輸入以篩選下方顯示的已知節目/角色列表。",
"new_char_input_placeholder_text":"新增節目/角色名稱",
"new_char_input_tooltip_text":"輸入新的節目、遊戲或角色名稱以新增至上方列表。",
"link_search_input_placeholder_text":"搜尋連結...",
"link_search_input_tooltip_text":"在「僅限連結」模式下，在此處輸入以按文字、網址或平台篩選顯示的連結。",
"manga_date_prefix_input_placeholder_text":"漫畫檔名前綴",
"manga_date_prefix_input_tooltip_text":"可選的「基於日期」或「原始檔案」漫畫檔名前綴（例如：「系列名稱」）。\n如果為空，檔案將根據樣式命名，不帶前綴。",
"log_display_mode_links_view_text":"🔗 連結檢視",
"log_display_mode_progress_view_text":"⬇️ 進度檢視",
"download_external_links_dialog_title":"下載所選的外部連結",
"select_all_button_text":"全選",
"deselect_all_button_text":"取消全選",
"cookie_browse_button_tooltip":"瀏覽 cookie 檔案（Netscape 格式，通常是 cookies.txt）。\n如果勾選「使用 Cookie」且上方的文字欄位為空，則將使用此檔案。",
"page_range_label_text":"頁面範圍：",
"start_page_input_placeholder":"開始",
"start_page_input_tooltip":"對於創作者網址：指定要下載的起始頁碼（例如：1、2、3）。\n留空或設為 1 以從第一頁開始。\n對於單一貼文網址或在漫畫/漫畫模式下停用。",
"page_range_to_label_text":"到",
"end_page_input_placeholder":"結束",
"end_page_input_tooltip":"對於創作者網址：指定要下載的結束頁碼（例如：5、10）。\n留空以下載從起始頁開始的所有頁面。\n對於單一貼文網址或在漫畫/漫畫模式下停用。",
"known_names_help_button_tooltip_text":"開啟應用程式功能指南。",
"future_settings_button_tooltip_text":"開啟應用程式設定（主題、語言等）。",
"link_search_button_tooltip_text":"篩選顯示的連結",
"confirm_add_all_dialog_title":"確認新增名稱",
"confirm_add_all_info_label":"您「按角色篩選」輸入中的以下新名稱/群組不在「Known.txt」中。\n新增它們可以改善未來下載的資料夾組織。\n\n請檢視列表並選擇操作：",
"confirm_add_all_select_all_button":"全選",
"confirm_add_all_deselect_all_button":"取消全選",
"confirm_add_all_add_selected_button":"將所選新增至 Known.txt",
"confirm_add_all_skip_adding_button":"跳過新增這些",
"confirm_add_all_cancel_download_button":"取消下載",
"cookie_help_dialog_title":"Cookie 檔案說明",
"cookie_help_instruction_intro":"<p>要使用 cookie，您通常需要瀏覽器中的 <b>cookies.txt</b> 檔案。</p>",
"cookie_help_how_to_get_title":"<p><b>如何取得 cookies.txt：</b></p>",
"cookie_help_step1_extension_intro":"<li>為您的 Chrome 瀏覽器安裝「Get cookies.txt LOCALLY」擴充功能：<br><a href=\"https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc\" style=\"color: #87CEEB;\">在 Chrome 線上應用程式商店取得 Get cookies.txt LOCALLY</a></li>",
"cookie_help_step2_login":"<li>前往網站（例如 kemono.su 或 coomer.su）並在需要時登入。</li>",
"cookie_help_step3_click_icon":"<li>點擊瀏覽器工具列中的擴充功能圖示。</li>",
"cookie_help_step4_export":"<li>點擊「匯出」按鈕（例如「匯出為」、「匯出 cookies.txt」 - 確切的措辭可能因擴充功能版本而異）。</li>",
"cookie_help_step5_save_file":"<li>將下載的 <code>cookies.txt</code> 檔案儲存到您的電腦。</li>",
"cookie_help_step6_app_intro":"<li>在此應用程式中：<ul>",
"cookie_help_step6a_checkbox":"<li>確保勾選「使用 Cookie」核取方塊。</li>",
"cookie_help_step6b_browse":"<li>點擊 cookie 文字欄位旁邊的「瀏覽...」按鈕。</li>",
"cookie_help_step6c_select":"<li>選擇您剛儲存的 <code>cookies.txt</code> 檔案。</li></ul></li>",
"cookie_help_alternative_paste":"<p>或者，某些擴充功能可能允許您直接複製 cookie 字串。如果是這樣，您可以將其貼到文字欄位中，而不是瀏覽檔案。</p>",
"cookie_help_proceed_without_button":"不使用 Cookie 下載",
"empty_popup_button_tooltip_text": "開啟創作者選擇 (瀏覽 creators.json)",
"cookie_help_cancel_download_button":"取消下載",
"character_input_tooltip":"輸入角色名稱（以逗號分隔）。支援進階分組，並在啟用「分開資料夾」時影響資料夾命名。\n\n範例：\n- Nami → 符合「Nami」，建立「Nami」資料夾。\n- (Ulti, Vivi) → 符合其中一個，資料夾「Ulti Vivi」，並分別將兩者新增至 Known.txt。\n- (Boa, Hancock)~ → 符合其中一個，資料夾「Boa Hancock」，並在 Known.txt 中新增為群組。\n\n名稱被視為用於比對的別名。\n\n篩選模式（按鈕切換）：\n- 檔案：按檔名篩選。\n- 標題：按貼文標題篩選。\n- 兩者：先標題，後檔名。\n- 留言 (Beta)：先檔名，後貼文留言。",
"tour_dialog_title":"歡迎使用 Kemono Downloader！",
"tour_dialog_never_show_checkbox":"不再顯示此導覽",
"tour_dialog_skip_button":"跳過導覽",
"tour_dialog_back_button":"返回",
"tour_dialog_next_button":"下一步",
"tour_dialog_finish_button":"完成",
"tour_dialog_step1_title":"👋 歡迎！",
"tour_dialog_step1_content":"您好！此快速導覽將引導您了解 Kemono Downloader 的主要功能，包括增強的篩選、改進的漫畫模式和 cookie 管理等最新更新。\n<ul>\n<li>我的目標是幫助您輕鬆地從 <b>Kemono</b> 和 <b>Coomer</b> 下載內容。</li><br>\n<li><b>🎨 創作者選擇按鈕：</b>在網址輸入旁邊，點擊調色盤圖示以開啟對話方塊。瀏覽並從您的 <code>creators.json</code> 檔案中選擇創作者，以快速將他們的名稱新增至網址輸入中。</li><br>\n<li><b>重要提示：應用程式「（沒有回應）」？</b><br>\n點擊「開始下載」後，特別是對於大型創作者動態或使用大量執行緒時，應用程式可能會暫時顯示為「（沒有回應）」。您的作業系統（Windows、macOS、Linux）甚至可能建議您「結束處理程序」或「強制結束」。<br>\n<b>請耐心等候！</b>應用程式通常仍在背景努力工作。在強制關閉之前，請嘗試在檔案總管中檢查您選擇的「下載位置」。如果您看到正在建立新資料夾或出現檔案，則表示下載正在正常進行。請給它一些時間恢復回應。</li><br>\n<li>使用<b>下一步</b>和<b>返回</b>按鈕進行導覽。</li><br>\n<li>將滑鼠懸停在許多選項上可獲得更多詳細資訊的工具提示。</li><br>\n<li>隨時點擊<b>跳過導覽</b>以關閉本指南。</li><br>\n<li>如果您不希望在未來啟動時看到此導覽，請勾選<b>「不再顯示此導覽」</b>。</li>\n</ul>",
"tour_dialog_step2_title":"① 開始使用",
"tour_dialog_step2_content":"讓我們從下載的基礎開始：\n<ul>\n<li><b>🔗 Kemono 創作者/貼文網址：</b><br>\n貼上創作者頁面（例如：<i>https://kemono.su/patreon/user/12345</i>）\n或特定貼文（例如：<i>.../post/98765</i>）的完整網址。<br>\n或 Coomer 創作者（例如：<i>https://coomer.su/onlyfans/user/artistname</i>）</li><br>\n<li><b>📁 下載位置：</b><br>\n點擊「瀏覽...」以選擇您電腦上要儲存所有下載檔案的資料夾。\n除非您使用「僅限連結」模式，否則此欄位為必填。</li><br>\n<li><b>📄 頁面範圍（僅限創作者網址）：</b><br>\n如果從創作者頁面下載，您可以指定要擷取的頁面範圍（例如：第 2 頁到第 5 頁）。\n留空則為所有頁面。對於單一貼文網址或啟用<b>漫畫/漫畫模式</b>時，此選項會停用。</li>\n</ul>",
"tour_dialog_step3_title":"② 篩選下載",
"tour_dialog_step3_content":"使用這些篩選器來精簡您要下載的內容（在「僅限連結」或「僅限壓縮檔」模式下，大多數篩選器會停用）：\n<ul>\n<li><b>🎯 按角色篩選：</b><br>\n輸入角色名稱，以逗號分隔（例如：<i>Tifa, Aerith</i>）。將別名分組以取得組合的資料夾名稱：<i>(alias1, alias2, alias3)</i> 會變成「alias1 alias2 alias3」資料夾（經過清理）。群組中的所有名稱都用作比對的別名。<br>\n此輸入旁邊的<b>「篩選：[類型]」</b>按鈕可切換此篩選器的應用方式：\n<ul><li><i>篩選：檔案：</i>檢查個別檔名。如果任何檔案符合條件，則保留該貼文；僅下載符合條件的檔案。資料夾命名使用符合條件的檔案名稱中的角色（如果啟用「分開資料夾」）。</li><br>\n<li><i>篩選：標題：</i>檢查貼文標題。符合條件的貼文中的所有檔案都將被下載。資料夾命名使用符合條件的貼文標題中的角色。</li>\n<li><b>⤵️ 新增至篩選器按鈕（已知名稱）：</b>在「已知名稱」的「新增」按鈕旁邊（請參閱步驟 5），這會開啟一個彈出視窗。透過核取方塊（附有搜尋列）從您的 <code>Known.txt</code> 列表中選擇名稱，以快速將它們新增至「按角色篩選」欄位。從 Known.txt 中分組的名稱，例如 <code>(Boa, Hancock)</code>，將以 <code>(Boa, Hancock)~</code> 的形式新增至篩選器。</li><br>\n<li><i>篩選：兩者：</i>先檢查貼文標題。如果符合，則下載所有檔案。如果不符合，則檢查檔名，並且僅下載符合條件的檔案。資料夾命名優先考慮標題符合，然後是檔案符合。</li><br>\n<li><i>篩選：留言 (Beta)：</i>先檢查檔名。如果檔案符合，則下載該貼文的所有檔案。如果沒有檔案符合，則檢查貼文留言。如果留言符合，則下載所有檔案。（使用更多 API 請求）。資料夾命名優先考慮檔案符合，然後是留言符合。</li></ul>\n如果啟用「按名稱/標題分開資料夾」，此篩選器也會影響資料夾命名。</li><br>\n<li><b>🚫 使用關鍵字跳過：</b><br>\n輸入單字，以逗號分隔（例如：<i>WIP, draft, preview</i>）。\n此輸入旁邊的<b>「範圍：[類型]」</b>按鈕可切換此篩選器的應用方式：\n<ul><li><i>範圍：檔案：</i>如果檔案名稱包含任何這些單字，則跳過檔案。</li><br>\n<li><i>範圍：貼文：</i>如果貼文標題包含任何這些單字，則跳過整個貼文。</li><br>\n<li><i>範圍：兩者：</i>同時應用檔案和貼文標題跳過（先貼文，後檔案）。</li></ul></li><br>\n<li><b>篩選檔案（選項按鈕）：</b>選擇要下載的內容：\n<ul>\n<li><i>全部：</i>下載所有找到的檔案類型。</li><br>\n<li><i>圖片/GIF：</i>僅限常見的圖片格式和 GIF。</li><br>\n<li><i>影片：</i>僅限常見的影片格式。</li><br>\n<li><b><i>📦 僅限壓縮檔：</i></b>專門下載 <b>.zip</b> 和 <b>.rar</b> 檔案。選擇此選項後，「跳過 .zip」和「跳過 .rar」核取方塊會自動停用並取消勾選。「顯示外部連結」也會停用。</li><br>\n<li><i>🎧 僅限音訊：</i>僅限常見的音訊格式（MP3、WAV、FLAC 等）。</li><br>\n<li><i>🔗 僅限連結：</i>從貼文描述中提取並顯示外部連結，而不是下載檔案。與下載相關的選項和「顯示外部連結」會停用。</li>\n</ul></li>\n</ul>",
"tour_dialog_step4_title":"③ 最愛模式（替代下載）",
"tour_dialog_step4_content":"應用程式提供「最愛模式」來下載您在 Kemono.su 上收藏的藝術家的內容。\n<ul>\n<li><b>⭐ 最愛模式核取方塊：</b><br>\n位於「🔗 僅限連結」選項按鈕旁邊。勾選此方塊以啟用最愛模式。</li><br>\n<li><b>最愛模式中的變化：</b>\n<ul><li>「🔗 Kemono 創作者/貼文網址」輸入區域會被一條訊息取代，表示最愛模式已啟用。</li><br>\n<li>標準的「開始下載」、「暫停」、「取消」按鈕會被「🖼️ 最愛的藝術家」和「📄 最愛的貼文」按鈕取代（注意：「最愛的貼文」功能計畫於未來推出）。</li><br>\n<li>「🍪 使用 Cookie」選項會自動啟用並鎖定，因為需要 cookie 來擷取您的最愛。</li></ul></li><br>\n<li><b>🖼️ 最愛的藝術家按鈕：</b><br>\n點擊此處可開啟一個對話方塊，列出您在 Kemono.su 上最愛的藝術家。您可以選擇一位或多位藝術家進行下載。</li><br>\n<li><b>最愛下載範圍（按鈕）：</b><br>\n此按鈕（位於「最愛的貼文」旁邊）控制所選最愛的下載位置：\n<ul><li><i>範圍：所選位置：</i>所有選定的藝術家都將下載到您設定的主要「下載位置」。篩選器會全域應用。</li><br>\n<li><i>範圍：藝術家資料夾：</i>在您的主要「下載位置」內為每位選定的藝術家建立一個子資料夾（以藝術家姓名命名）。該藝術家的內容將進入其特定資料夾。篩選器會在每個藝術家的資料夾內應用。</li></ul></li><br>\n<li><b>最愛模式中的篩選器：</b><br>\n「按角色篩選」、「使用關鍵字跳過」和「篩選檔案」選項仍適用於從您選定的最愛藝術家下載的內容。</li>\n</ul>",
"tour_dialog_step5_title":"④ 微調下載",
"tour_dialog_step5_content":"更多選項可自訂您的下載：\n<ul>\n<li><b>跳過 .zip / 跳過 .rar：</b>勾選這些方塊以避免下載這些壓縮檔類型。\n<i>（注意：如果選擇「📦 僅限壓縮檔」篩選模式，它們會被停用並忽略）。</i></li><br>\n<li><b>✂️ 從名稱中移除單字：</b><br>\n輸入單字，以逗號分隔（例如：<i>patreon, [HD]</i>），以從下載的檔案名稱中移除（不區分大小寫）。</li><br>\n<li><b>僅下載縮圖：</b>下載小型預覽圖而不是完整大小的檔案（如果可用）。</li><br>\n<li><b>壓縮大型圖片：</b>如果安裝了「Pillow」庫，大於 1.5MB 的圖片將轉換為 WebP 格式（如果 WebP 版本明顯較小）。</li><br>\n<li><b>🗄️ 自訂資料夾名稱（僅限單一貼文）：</b><br>\n如果您正在下載特定貼文網址且已啟用「按名稱/標題分開資料夾」，\n您可以在此處為該貼文的下載資料夾輸入自訂名稱。</li><br>\n<li><b>🍪 使用 Cookie：</b>勾選此方塊以使用 cookie 進行請求。您可以：\n<ul><li>直接在文字欄位中輸入 cookie 字串（例如：<i>name1=value1; name2=value2</i>）。</li><br>\n<li>點擊「瀏覽...」以選擇 <i>cookies.txt</i> 檔案（Netscape 格式）。路徑將顯示在文字欄位中。</li></ul>\n這對於存取需要登入的內容很有用。如果已填寫，文字欄位優先。\n如果勾選「使用 Cookie」，但文字欄位和瀏覽的檔案都為空，它將嘗試從應用程式目錄載入「cookies.txt」。</li>\n</ul>",
"tour_dialog_step6_title":"⑤ 組織與效能",
"tour_dialog_step6_content":"組織您的下載並管理效能：\n<ul>\n<li><b>⚙️ 按名稱/標題分開資料夾：</b>根據「按角色篩選」輸入或貼文標題建立子資料夾（可使用 <b>Known.txt</b> 列表作為資料夾名稱的備用）。</li><br>\n<li><b>每個貼文一個子資料夾：</b>如果啟用「分開資料夾」，這會在主要的角色/標題資料夾內為<i>每個個別貼文</i>建立一個額外的子資料夾。</li><br>\n<li><b>🚀 使用多執行緒（執行緒）：</b>啟用更快的操作。「執行緒」輸入中的數字表示：\n<ul><li>對於<b>創作者動態：</b>同時處理的貼文數量。每個貼文中的檔案由其工作執行緒按順序下載（除非啟用「基於日期」的漫畫命名，這會強制使用 1 個貼文工作執行緒）。</li><br>\n<li>對於<b>單一貼文網址：</b>從該單一貼文同時下載的檔案數量。</li></ul>\n如果未勾選，則使用 1 個執行緒。高執行緒計數（例如 >40）可能會顯示警告。</li><br>\n<li><b>多部分下載切換（日誌區域右上角）：</b><br>\n<b>「多部分：[開啟/關閉]」</b>按鈕可讓您為單個大型檔案啟用/停用多分段下載。\n<ul><li><b>開啟：</b>可以加快大型檔案（例如影片）的下載速度，但可能會增加 UI 不穩定性或對於許多小檔案造成日誌垃圾訊息。啟用時會出現警告。如果多部分下載失敗，它會以單一串流重試。</li><br>\n<li><b>關閉（預設）：</b>檔案以單一串流下載。</li></ul>\n如果「僅限連結」或「僅限壓縮檔」模式處於活動狀態，則此選項會停用。</li><br>\n<li><b>📖 漫畫/漫畫模式（僅限創作者網址）：</b>專為循序內容設計。\n<ul>\n<li>從<b>最舊到最新</b>下載貼文。</li><br>\n<li>「頁面範圍」輸入會停用，因為會擷取所有貼文。</li><br>\n<li>當此模式對於創作者動態處於活動狀態時，日誌區域的右上角會出現一個<b>檔名樣式切換按鈕</b>（例如：「命名：貼文標題」）。點擊它可在命名樣式之間切換：\n<ul>\n<li><b><i>命名：貼文標題（預設）：</i></b>貼文中的第一個檔案根據清理後的貼文標題命名（例如：「我的第一章.jpg」）。<i>同一貼文</i>中的後續檔案將嘗試保留其原始檔名（例如：「page_02.png」、「bonus_art.jpg」）。如果貼文只有一個檔案，它將根據貼文標題命名。這通常是大多數漫畫/漫畫的建議選項。</li><br>\n<li><b><i>命名：原始檔案：</i></b>所有檔案都嘗試保留其原始檔名。可以在樣式按鈕旁邊出現的輸入欄位中輸入可選的前綴（例如：「我的系列_」）。範例：「我的系列_原始檔案.jpg」。</li><br>\n<li><b><i>命名：標題+全域編號（貼文標題+全域編號）：</i></b>目前下載工作階段中所有貼文的所有檔案都使用清理後的貼文標題作為前綴，後面跟著一個全域計數器，按順序命名。例如：貼文「第一章」（2 個檔案）-> 「第一章_001.jpg」、「第一章_002.png」。下一個貼文「第二章」（1 個檔案）將繼續編號 -> 「第二章_003.jpg」。此樣式會自動停用貼文處理的多執行緒，以確保正確的全域編號。</li><br>\n<li><b><i>命名：基於日期：</i></b>檔案根據貼文的發布順序按順序命名（001.ext、002.ext、...）。可以在樣式按鈕旁邊出現的輸入欄位中輸入可選的前綴（例如：「我的系列_」）。範例：「我的系列_001.jpg」。此樣式會自動停用貼文處理的多執行緒。</li>\n</ul>\n</li><br>\n<li>為獲得「命名：貼文標題」、「命名：標題+全域編號」或「命名：基於日期」樣式的最佳效果，請在「按角色篩選」欄位中使用漫畫/系列標題進行資料夾組織。</li>\n</ul></li><br>\n<li><b>🎭 Known.txt 用於智慧資料夾組織：</b><br>\n<code>Known.txt</code>（位於應用程式目錄中）可在啟用「按名稱/標題分開資料夾」時對自動資料夾組織進行精細控制。\n<ul>\n<li><b>運作方式：</b><code>Known.txt</code> 中的每一行都是一個條目。\n<ul><li>像 <code>我的精彩系列</code> 這樣的單行表示符合此內容的內容將進入名為「我的精彩系列」的資料夾。</li><br>\n<li>像 <code>(角色 A, 角 A, 備用名稱 A)</code> 這樣的群組行表示符合「角色 A」、「角 A」或「備用名稱 A」的內容都將進入一個名為「角色 A 角 A 備用名稱 A」的資料夾（經過清理）。括號中的所有術語都成為該資料夾的別名。</li></ul></li>\n<li><b>智慧備用：</b>啟用「按名稱/標題分開資料夾」時，如果貼文不符合任何特定的「按角色篩選」條目，下載器會查詢 <code>Known.txt</code> 以尋找用於建立資料夾的主要符合名稱。</li><br>\n<li><b>使用者友善的管理：</b>透過下方的 UI 列表新增簡單（非群組）名稱。對於進階編輯（例如建立/修改群組別名），點擊<b>「開啟 Known.txt」</b>以在您的文字編輯器中編輯檔案。應用程式會在下次使用或啟動時重新載入它。</li>\n</ul>\n</li>\n</ul>",
"tour_dialog_step7_title":"⑥ 常見錯誤與疑難排解",
"tour_dialog_step7_content":"有時下載可能會遇到問題。以下是一些常見問題：\n<ul>\n<li><b>角色輸入工具提示：</b><br>\n輸入角色名稱，以逗號分隔（例如：<i>Tifa, Aerith</i>）。<br>\n將別名分組以取得組合的資料夾名稱：<i>(alias1, alias2, alias3)</i> 會變成「alias1 alias2 alias3」資料夾。<br>\n群組中的所有名稱都用作符合內容的別名。<br><br>\n此輸入旁邊的「篩選：[類型]」按鈕可切換此篩選器的應用方式：<br>\n- 篩選：檔案：檢查個別檔名。僅下載符合條件的檔案。<br>\n- 篩選：標題：檢查貼文標題。符合條件的貼文中的所有檔案都將被下載。<br>\n- 篩選：兩者：先檢查貼文標題。如果不符合，則檢查檔名。<br>\n- 篩選：留言 (Beta)：先檢查檔名。如果不符合，則檢查貼文留言。<br><br>\n如果啟用「按名稱/標題分開資料夾」，此篩選器也會影響資料夾命名。</li><br>\n<li><b>502 Bad Gateway / 503 Service Unavailable / 504 Gateway Timeout：</b><br>\n這通常表示 Kemono/Coomer 伺服器端有暫時性問題。網站可能過載、正在維護或遇到問題。<br>\n<b>解決方案：</b>稍候片刻（例如 30 分鐘到幾小時），然後再試一次。直接在瀏覽器中檢查網站。</li><br>\n<li><b>連線中斷 / 連線被拒 / 逾時（在下載檔案期間）：</b><br>\n這可能是由於您的網際網路連線、伺服器不穩定或伺服器中斷大型檔案的連線所致。<br>\n<b>解決方案：</b>檢查您的網際網路。如果「執行緒」數量較高，請嘗試降低它。應用程式可能會在工作階段結束時提示您重試某些失敗的檔案。</li><br>\n<li><b>IncompleteRead 錯誤：</b><br>\n伺服器傳送的資料少於預期。通常是暫時的網路或伺服器問題。<br>\n<b>解決方案：</b>應用程式通常會將這些檔案標記為在下載工作階段結束時重試。</li><br>\n<li><b>403 Forbidden / 401 Unauthorized（對於公開貼文較不常見）：</b><br>\n您可能無權存取內容。對於某些付費或私人內容，使用「使用 Cookie」選項搭配瀏覽器工作階段中的有效 cookie 可能會有所幫助。請確保您的 cookie 是最新的。</li><br>\n<li><b>404 Not Found：</b><br>\n貼文或檔案網址不正確，或內容已從網站移除。請再次檢查網址。</li><br>\n<li><b>「找不到貼文」/「找不到目標貼文」：</b><br>\n請確保網址正確且創作者/貼文存在。如果使用頁面範圍，請確保它們對於該創作者是有效的。對於非常新的貼文，在它們出現在 API 中之前可能會有一點延遲。</li><br>\n<li><b>一般緩慢 / 應用程式「（沒有回應）」：</b><br>\n如步驟 1 所述，如果應用程式在啟動後似乎凍結，特別是對於大型創作者動態或大量執行緒，請給它一些時間。它可能正在背景處理資料。如果這種情況頻繁發生，降低執行緒計數有時可以改善回應性。</li>\n</ul>",
"tour_dialog_step8_title":"⑦ 日誌與最終控制",
"tour_dialog_step8_content":"監控與控制：\n<ul>\n<li><b>📜 進度日誌 / 提取的連結日誌：</b>顯示詳細的下載訊息。如果啟用「🔗 僅限連結」模式，此區域會顯示提取的連結。</li><br>\n<li><b>在日誌中顯示外部連結：</b>如果勾選，主日誌下方會出現一個次要日誌面板，用於顯示在貼文描述中找到的任何外部連結。<i>（如果啟用「🔗 僅限連結」或「📦 僅限壓縮檔」模式，則此選項會停用）。</i></li><br>\n<li><b>日誌檢視切換（👁️ / 🙈 按鈕）：</b><br>\n此按鈕（位於日誌區域的右上角）可切換主日誌的檢視：\n<ul><li><b>👁️ 進度日誌（預設）：</b>顯示所有下載活動、錯誤和摘要。</li><br>\n<li><b>🙈 遺漏的角色日誌：</b>顯示因您的「按角色篩選」設定而跳過的貼文標題中的關鍵字列表。有助於識別您可能無意中遺漏的內容。</li></ul></li><br>\n<li><b>🔄 重設：</b>清除所有輸入欄位、日誌並將臨時設定重設為預設值。僅在沒有下載活動時才能使用。</li><br>\n<li><b>⬇️ 開始下載 / 🔗 提取連結 / ⏸️ 暫停 / ❌ 取消：</b>這些按鈕控制流程。「取消並重設介面」會停止目前的操作並執行軟性介面重設，保留您的網址和目錄輸入。「暫停/繼續」可讓您暫時停止和繼續。</li><br>\n<li>如果某些檔案因可恢復的錯誤（例如「IncompleteRead」）而失敗，系統可能會在工作階段結束時提示您重試。</li>\n</ul>\n<br>您已準備就緒！點擊<b>「完成」</b>以關閉導覽並開始使用下載器。",
"help_guide_dialog_title":"Kemono Downloader - 功能指南",
"help_guide_github_tooltip":"訪問 GitHub 上的專案頁面（在瀏覽器中開啟）",
"help_guide_instagram_tooltip":"訪問我們的 Instagram 頁面（在瀏覽器中開啟）",
"help_guide_discord_tooltip":"訪問我們的 Discord 社群（在瀏覽器中開啟）",
"help_guide_step1_title":"① 簡介與主要輸入",
"help_guide_step1_content":"<html><head/><body>\n<p>本指南概述了 Kemono Downloader 的功能、欄位和按鈕。</p>\n<h3>主要輸入區（左上角）</h3>\n<ul>\n<li><b>🔗 Kemono 創作者/貼文網址：</b>\n<ul>\n<li>輸入創作者頁面（例如：<i>https://kemono.su/patreon/user/12345</i>）或特定貼文（例如：<i>.../post/98765</i>）的完整網址。</li>\n<li>支援 Kemono（kemono.su、kemono.party）和 Coomer（coomer.su、coomer.party）的網址。</li>\n</ul>\n</li>\n<li><b>頁面範圍（開始到結束）：</b>\n<ul>\n<li>對於創作者網址：指定要擷取的頁面範圍（例如：第 2 頁到第 5 頁）。留空則為所有頁面。</li>\n<li>對於單一貼文網址或啟用<b>漫畫/漫畫模式</b>時停用。</li>\n</ul>\n</li>\n<li><b>📁 下載位置：</b>\n<ul>\n<li>點擊<b>「瀏覽...」</b>以選擇您電腦上要儲存所有下載檔案的主要資料夾。</li>\n<li>除非您使用<b>「🔗 僅限連結」</b>模式，否則此欄位為必填。</li>\n</ul>\n</li>\n<li><b>🎨 創作者選擇按鈕（網址輸入旁邊）：</b>\n<ul>\n<li>點擊調色盤圖示（🎨）以開啟「創作者選擇」對話方塊。</li>\n<li>此對話方塊會從您的 <code>creators.json</code> 檔案（應位於應用程式目錄中）載入創作者。</li>\n<li><b>對話方塊內部：</b>\n<ul>\n<li><b>搜尋列：</b>輸入以按名稱或服務篩選創作者列表。</li>\n<li><b>創作者列表：</b>顯示您 <code>creators.json</code> 中的創作者。您收藏的創作者（在 JSON 資料中）會顯示在最上方。</li>\n<li><b>核取方塊：</b>透過勾選創作者姓名旁邊的方塊來選擇一位或多位創作者。</li>\n<li><b>「範圍」按鈕（例如：「範圍：角色」）：</b>此按鈕可切換從此彈出視窗啟動下載時的下載組織：\n<ul><li><i>範圍：角色：</i>下載將直接在您的主要「下載位置」中組織到以角色命名的資料夾中。來自不同創作者的相同角色的作品將被分組在一起。</li>\n<li><i>範圍：創作者：</i>下載將首先在您的主要「下載位置」內建立一個以創作者命名的資料夾。然後，以角色命名的子資料夾將在每個創作者的資料夾內建立。</li></ul>\n</li>\n<li><b>「新增所選」按鈕：</b>點擊此處將取得所有已勾選創作者的名稱，並將它們以逗號分隔的方式新增至主要的「🔗 Kemono 創作者/貼文網址」輸入欄位中。然後對話方塊將關閉。</li>\n</ul>\n</li>\n<li>此功能提供了一種快速填寫多位創作者網址欄位的方法，無需手動輸入或貼上每個網址。</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step2_title":"② 篩選下載",
"help_guide_step2_content":"<html><head/><body>\n<h3>篩選下載（左側面板）</h3>\n<ul>\n<li><b>🎯 按角色篩選：</b>\n<ul>\n<li>輸入名稱，以逗號分隔（例如：<code>Tifa, Aerith</code>）。</li>\n<li><b>共用資料夾的群組別名（在 Known.txt 中為獨立條目）：</b><code>(Vivi, Ulti, Uta)</code>。\n<ul><li>符合「Vivi」、「Ulti」或「Uta」的內容將進入名為「Vivi Ulti Uta」的共用資料夾（經過清理）。</li>\n<li>如果這些名稱是新的，系統會提示您將「Vivi」、「Ulti」和「Uta」作為<i>獨立的個別條目</i>新增至 <code>Known.txt</code>。</li>\n</ul>\n</li>\n<li><b>共用資料夾的群組別名（在 Known.txt 中為單一條目）：</b><code>(Yuffie, Sonon)~</code>（注意波浪號 <code>~</code>）。\n<ul><li>符合「Yuffie」或「Sonon」的內容將進入名為「Yuffie Sonon」的共用資料夾。</li>\n<li>如果為新名稱，系統會提示將「Yuffie Sonon」（及其別名 Yuffie、Sonon）作為<i>單一的群組條目</i>新增至 <code>Known.txt</code>。</li>\n</ul>\n</li>\n<li>如果啟用「按名稱/標題分開資料夾」，此篩選器會影響資料夾命名。</li>\n</ul>\n</li>\n<li><b>篩選：[類型] 按鈕（角色篩選範圍）：</b>切換「按角色篩選」的應用方式：\n<ul>\n<li><code>篩選：檔案</code>：檢查個別檔名。如果任何檔案符合條件，則保留該貼文；僅下載符合條件的檔案。資料夾命名使用符合條件的檔案名稱中的角色。</li>\n<li><code>篩選：標題</code>：檢查貼文標題。符合條件的貼文中的所有檔案都將被下載。資料夾命名使用符合條件的貼文標題中的角色。</li>\n<li><code>篩選：兩者</code>：先檢查貼文標題。如果符合，則下載所有檔案。如果不符合，則檢查檔名，並且僅下載符合條件的檔案。資料夾命名優先考慮標題符合，然後是檔案符合。</li>\n<li><code>篩選：留言 (Beta)</code>：先檢查檔名。如果檔案符合，則下載該貼文的所有檔案。如果沒有檔案符合，則檢查貼文留言。如果留言符合，則下載所有檔案。（使用更多 API 請求）。資料夾命名優先考慮檔案符合，然後是留言符合。</li>\n</ul>\n</li>\n<li><b>🗄️ 自訂資料夾名稱（僅限單一貼文）：</b>\n<ul>\n<li>僅在下載特定貼文網址且啟用「按名稱/標題分開資料夾」時可見並可用。</li>\n<li>可讓您為該單一貼文的下載資料夾指定自訂名稱。</li>\n</ul>\n</li>\n<li><b>🚫 使用關鍵字跳過：</b>\n<ul><li>輸入單字，以逗號分隔（例如：<code>WIP, draft, preview</code>）以跳過某些內容。</li></ul>\n</li>\n<li><b>範圍：[類型] 按鈕（跳過單字範圍）：</b>切換「使用關鍵字跳過」的應用方式：\n<ul>\n<li><code>範圍：檔案</code>：如果個別檔案的名稱包含任何這些單字，則跳過這些檔案。</li>\n<li><code>範圍：貼文</code>：如果貼文標題包含任何這些單字，則跳過整個貼文。</li>\n<li><code>範圍：兩者</code>：同時應用兩者（先貼文標題，後個別檔案）。</li>\n</ul>\n</li>\n<li><b>✂️ 從名稱中移除單字：</b>\n<ul><li>輸入單字，以逗號分隔（例如：<code>patreon, [HD]</code>），以從下載的檔案名稱中移除（不區分大小寫）。</li></ul>\n</li>\n<li><b>篩選檔案（選項按鈕）：</b>選擇要下載的內容：\n<ul>\n<li><code>全部</code>：下載所有找到的檔案類型。</li>\n<li><code>圖片/GIF</code>：僅限常見的圖片格式（JPG、PNG、GIF、WEBP 等）和 GIF。</li>\n<li><code>影片</code>：僅限常見的影片格式（MP4、MKV、WEBM、MOV 等）。</li>\n<li><code>📦 僅限壓縮檔</code>：專門下載 <b>.zip</b> 和 <b>.rar</b> 檔案。選擇此選項後，「跳過 .zip」和「跳過 .rar」核取方塊會自動停用並取消勾選。「顯示外部連結」也會停用。</li>\n<li><code>🎧 僅限音訊</code>：僅下載常見的音訊格式（MP3、WAV、FLAC、M4A、OGG 等）。其他特定檔案選項的行為與「圖片」或「影片」模式類似。</li>\n<li><code>🔗 僅限連結</code>：從貼文描述中提取並顯示外部連結，而不是下載檔案。與下載相關的選項和「顯示外部連結」會停用。主要下載按鈕會變更為「🔗 提取連結」。</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step3_title":"③ 下載選項與設定",
"help_guide_step3_content":"<html><head/><body>\n<h3>下載選項與設定（左側面板）</h3>\n<ul>\n<li><b>跳過 .zip / 跳過 .rar：</b>核取方塊以避免下載這些壓縮檔類型。（如果選擇「📦 僅限壓縮檔」篩選模式，則停用並忽略）。</li>\n<li><b>僅下載縮圖：</b>下載小型預覽圖而不是完整大小的檔案（如果可用）。</li>\n<li><b>壓縮大型圖片（至 WebP）：</b>如果安裝了「Pillow」（PIL）庫，大於 1.5MB 的圖片將轉換為 WebP 格式（如果 WebP 版本明顯較小）。</li>\n<li><b>⚙️ 進階設定：</b>\n<ul>\n<li><b>按名稱/標題分開資料夾：</b>根據「按角色篩選」輸入或貼文標題建立子資料夾。可使用 <b>Known.txt</b> 列表作為資料夾名稱的備用選項。</li></ul></li></ul></body></html>",
"help_guide_step4_title":"④ 進階設定（第 1 部分）",
"help_guide_step4_content":"<html><head/><body><h3>⚙️ 進階設定（續）</h3><ul><ul>\n<li><b>每個貼文一個子資料夾：</b>如果啟用「分開資料夾」，這會在主要的角色/標題資料夾內為<i>每個個別貼文</i>建立一個額外的子資料夾。</li>\n<li><b>使用 Cookie：</b>勾選此方塊以使用 cookie 進行請求。\n<ul>\n<li><b>文字欄位：</b>直接輸入 cookie 字串（例如：<code>name1=value1; name2=value2</code>）。</li>\n<li><b>瀏覽...：</b>選擇 <code>cookies.txt</code> 檔案（Netscape 格式）。路徑將顯示在文字欄位中。</li>\n<li><b>優先順序：</b>文字欄位（如果已填寫）優先於瀏覽的檔案。如果勾選「使用 Cookie」，但兩者都為空，它將嘗試從應用程式目錄載入 <code>cookies.txt</code>。</li>\n</ul>\n</li>\n<li><b>使用多執行緒和執行緒輸入：</b>\n<ul>\n<li>啟用更快的操作。「執行緒」輸入中的數字表示：\n<ul>\n<li>對於<b>創作者動態：</b>同時處理的貼文數量。每個貼文中的檔案由其工作執行緒按順序下載（除非啟用「基於日期」的漫畫命名，這會強制使用 1 個貼文工作執行緒）。</li>\n<li>對於<b>單一貼文網址：</b>從該單一貼文同時下載的檔案數量。</li>\n</ul>\n</li>\n<li>如果未勾選，則使用 1 個執行緒。高執行緒計數（例如 >40）可能會顯示警告。</li>\n</ul>\n</li></ul></ul></body></html>",
"help_guide_step5_title":"⑤ 進階設定（第 2 部分）與操作",
"help_guide_step5_content":"<html><head/><body><h3>⚙️ 進階設定（續）</h3><ul><ul>\n<li><b>在日誌中顯示外部連結：</b>如果勾選，主日誌下方會出現一個次要日誌面板，用於顯示在貼文描述中找到的任何外部連結。（如果啟用「🔗 僅限連結」或「📦 僅限壓縮檔」模式，則停用）。</li>\n<li><b>📖 漫畫/漫畫模式（僅限創作者網址）：</b>專為循序內容設計。\n<ul>\n<li>從<b>最舊到最新</b>下載貼文。</li>\n<li>「頁面範圍」輸入會停用，因為會擷取所有貼文。</li>\n<li>當此模式對於創作者動態處於活動狀態且未處於「僅限連結」或「僅限壓縮檔」模式時，日誌區域的右上角會出現一個<b>檔名樣式切換按鈕</b>（例如：「命名：貼文標題」）。點擊它可在命名樣式之間切換：\n<ul>\n<li><code>命名：貼文標題（預設）</code>：貼文中的第一個檔案根據清理後的貼文標題命名（例如：「我的第一章.jpg」）。<i>同一貼文</i>中的後續檔案將嘗試保留其原始檔名（例如：「page_02.png」、「bonus_art.jpg」）。如果貼文只有一個檔案，它將根據貼文標題命名。這通常是大多數漫畫/漫畫的建議選項。</li>\n<li><code>命名：原始檔案</code>：所有檔案都嘗試保留其原始檔名。</li>\n<li><code>命名：原始檔案</code>：所有檔案都嘗試保留其原始檔名。當此樣式處於活動狀態時，此樣式按鈕旁邊會出現一個用於<b>可選檔名前綴</b>的輸入欄位（例如：「我的系列_」）。範例：「我的系列_原始檔案.jpg」。</li>\n<li><code>命名：標題+全域編號（貼文標題+全域編號）</code>：目前下載工作階段中所有貼文的所有檔案都使用清理後的貼文標題作為前綴，後面跟著一個全域計數器，按順序命名。範例：貼文「第一章」（2 個檔案）-> 「第一章 001.jpg」、「第一章 002.png」。下一個貼文「第二章」（1 個檔案）-> 「第二章 003.jpg」。此樣式會自動停用貼文處理的多執行緒。</li>\n<li><code>命名：基於日期</code>：檔案根據發布順序按順序命名（001.ext、002.ext、...）。當此樣式處於活動狀態時，此樣式按鈕旁邊會出現一個用於<b>可選檔名前綴</b>的輸入欄位（例如：「我的系列_」）。範例：「我的系列_001.jpg」。此樣式會自動停用貼文處理的多執行緒。</li>\n</ul>\n</li>\n<li>為獲得「命名：貼文標題」、「命名：標題+全域編號」或「命名：基於日期」樣式的最佳效果，請在「按角色篩選」欄位中使用漫畫/系列標題進行資料夾組織。</li>\n</ul>\n</li>\n</ul></li></ul>\n<h3>主要操作按鈕（左側面板）</h3>\n<ul>\n<li><b>⬇️ 開始下載 / 🔗 提取連結：</b>此按鈕的文字和功能根據「篩選檔案」選項按鈕的選擇而變更。它會啟動主要操作。</li>\n<li><b>⏸️ 暫停下載 / ▶️ 繼續下載：</b>可讓您暫時停止目前正在進行的下載/提取過程，並稍後繼續。某些 UI 設定可以在暫停時變更。</li>\n<li><b>❌ 取消並重設介面：</b>停止目前的操作並執行軟性介面重設。您的網址和下載目錄輸入將被保留，但其他設定和日誌將被清除。</li>\n</ul></body></html>",
"help_guide_step6_title":"⑥ 已知節目/角色列表",
"help_guide_step6_content":"<html><head/><body>\n<h3>管理已知節目/角色列表（左下角）</h3>\n<p>此部分有助於管理 <code>Known.txt</code> 檔案，該檔案用於啟用「按名稱/標題分開資料夾」時的智慧資料夾組織，特別是當貼文不符合您目前作用中的「按角色篩選」輸入時作為備用選項。</p>\n<ul>\n<li><b>開啟 Known.txt：</b>在您的預設文字編輯器中開啟 <code>Known.txt</code> 檔案（位於應用程式目錄中）以進行進階編輯（例如建立複雜的群組別名）。</li>\n<li><b>搜尋角色...：</b>篩選下方顯示的已知名稱列表。</li>\n<li><b>列表小工具：</b>顯示您 <code>Known.txt</code> 中的主要名稱。在此處選擇條目以刪除它們。</li>\n<li><b>新增新節目/角色名稱（輸入欄位）：</b>輸入要新增的名稱或群組。\n<ul>\n<li><b>單一名稱：</b>例如：<code>我的精彩系列</code>。作為單一條目新增。</li>\n<li><b>用於在 Known.txt 中建立獨立條目的群組：</b>例如：<code>(Vivi, Ulti, Uta)</code>。將「Vivi」、「Ulti」和「Uta」作為三個獨立的個別條目新增至 <code>Known.txt</code>。</li>\n<li><b>用於共用資料夾和在 Known.txt 中建立單一條目的群組（波浪號 <code>~</code>）：</b>例如：<code>(角色 A, 角 A)~</code>。在 <code>Known.txt</code> 中新增一個名為「角色 A 角 A」的條目。「角色 A」和「角 A」成為此單一資料夾/條目的別名。</li>\n</ul>\n</li>\n<li><b>➕ 新增按鈕：</b>將上方輸入欄位中的名稱/群組新增至列表和 <code>Known.txt</code>。</li>\n<li><b>⤵️ 新增至篩選器按鈕：</b>\n<ul>\n<li>位於「已知節目/角色」列表的「➕ 新增」按鈕旁邊。</li>\n<li>點擊此按鈕會開啟一個彈出視窗，顯示您 <code>Known.txt</code> 檔案中的所有名稱，每個名稱都有一個核取方塊。</li>\n<li>彈出視窗包含一個搜尋列，可快速篩選名稱列表。</li>\n<li>您可以使用核取方塊選擇一個或多個名稱。</li>\n<li>點擊「新增所選」將所選名稱插入主視窗中的「按角色篩選」輸入欄位中。</li>\n<li>如果從 <code>Known.txt</code> 中選擇的名稱最初是群組（例如：在 Known.txt 中定義為 <code>(Boa, Hancock)</code>），它將以 <code>(Boa, Hancock)~</code> 的形式新增至篩選欄位中。單一名稱則按原樣新增。</li>\n<li>為方便起見，彈出視窗中提供「全選」和「取消全選」按鈕。</li>\n<li>點擊「取消」以關閉彈出視窗而不進行任何變更。</li>\n</ul>\n</li>\n<li><b>🗑️ 刪除所選按鈕：</b>從列表和 <code>Known.txt</code> 中刪除所選名稱。</li>\n<li><b>❓ 按鈕（就是這個！）：</b>顯示此綜合說明指南。</li>\n</ul></body></html>",
"help_guide_step7_title":"⑦ 日誌區域與控制項",
"help_guide_step7_content":"<html><head/><body>\n<h3>日誌區域與控制項（右側面板）</h3>\n<ul>\n<li><b>📜 進度日誌 / 提取的連結日誌（標籤）：</b>主日誌區域的標題；如果啟用「🔗 僅限連結」模式，則會變更。</li>\n<li><b>搜尋連結... / 🔍 按鈕（連結搜尋）：</b>\n<ul><li>僅在啟用「🔗 僅限連結」模式時可見。可讓您即時按文字、網址或平台篩選主日誌中顯示的提取連結。</li></ul>\n</li>\n<li><b>命名：[樣式] 按鈕（漫畫檔名樣式）：</b>\n<ul><li>僅在<b>漫畫/漫畫模式</b>對於創作者動態處於活動狀態且未處於「僅限連結」或「僅限壓縮檔」模式時可見。</li>\n<li>在檔名樣式之間切換：<code>貼文標題</code>、<code>原始檔案</code>、<code>基於日期</code>。（有關詳細資訊，請參閱漫畫/漫畫模式部分）。</li>\n<li>當「原始檔案」或「基於日期」樣式處於活動狀態時，此按鈕旁邊會出現一個用於<b>可選檔名前綴</b>的輸入欄位。</li>\n</ul>\n</li>\n<li><b>多部分：[開啟/關閉] 按鈕：</b>\n<ul><li>為單個大型檔案切換多分段下載。\n<ul><li><b>開啟：</b>可以加快大型檔案（例如影片）的下載速度，但可能會增加 UI 不穩定性或對於許多小檔案造成日誌垃圾訊息。啟用時會出現警告。如果多部分下載失敗，它會以單一串流重試。</li>\n<li><b>關閉（預設）：</b>檔案以單一串流下載。</li>\n</ul>\n<li>如果啟用「🔗 僅限連結」或「📦 僅限壓縮檔」模式，則停用。</li>\n</ul>\n</li>\n<li><b>👁️ / 🙈 按鈕（日誌檢視切換）：</b>切換主日誌的檢視：\n<ul>\n<li><b>👁️ 進度日誌（預設）：</b>顯示所有下載活動、錯誤和摘要。</li>\n<li><b>🙈 遺漏的角色日誌：</b>顯示因您的「按角色篩選」設定而跳過的貼文標題/內容中的關鍵字列表。有助於識別您可能無意中遺漏的內容。</li>\n</ul>\n</li>\n<li><b>🔄 重設按鈕：</b>清除所有輸入欄位、日誌並將臨時設定重設為預設值。僅在沒有下載活動時才能使用。</li>\n<li><b>主日誌輸出（文字區域）：</b>顯示詳細的進度訊息、錯誤和摘要。如果啟用「🔗 僅限連結」模式，此區域會顯示提取的連結。</li>\n<li><b>遺漏的角色日誌輸出（文字區域）：</b>（透過 👁️ / 🙈 切換可見）顯示因角色篩選而跳過的貼文/檔案。</li>\n<li><b>外部日誌輸出（文字區域）：</b>如果勾選「在日誌中顯示外部連結」，則會出現在主日誌下方。顯示在貼文描述中找到的外部連結。</li>\n<li><b>匯出連結按鈕：</b>\n<ul><li>僅在啟用「🔗 僅限連結」模式且已提取連結時可見並啟用。</li>\n<li>可讓您將所有提取的連結儲存到 <code>.txt</code> 檔案。</li>\n</ul>\n</li>\n<li><b>進度：[狀態] 標籤：</b>顯示下載或連結提取過程的整體進度（例如：已處理的貼文）。</li>\n<li><b>檔案進度標籤：</b>顯示個別檔案下載的進度，包括速度和大小，或多部分下載狀態。</li>\n</ul></body></html>",
"help_guide_step8_title":"⑧ 最愛模式與未來功能",
"help_guide_step8_content":"<html><head/><body>\n<h3>最愛模式（從您在 Kemono.su 上的最愛下載）</h3>\n<p>此模式可讓您直接從您在 Kemono.su 上收藏的藝術家下載內容。</p>\n<ul>\n<li><b>⭐ 如何啟用：</b>\n<ul>\n<li>勾選<b>「⭐ 最愛模式」</b>核取方塊，位於「🔗 僅限連結」選項按鈕旁邊。</li>\n</ul>\n</li>\n<li><b>最愛模式中的 UI 變更：</b>\n<ul>\n<li>「🔗 Kemono 創作者/貼文網址」輸入區域會被一條訊息取代，表示最愛模式已啟用。</li>\n<li>標準的「開始下載」、「暫停」、「取消」按鈕會被以下按鈕取代：\n<ul>\n<li><b>「🖼️ 最愛的藝術家」</b>按鈕</li>\n<li><b>「📄 最愛的貼文」</b>按鈕</li>\n</ul>\n</li>\n<li>「🍪 使用 Cookie」選項會自動啟用並鎖定，因為需要 cookie 來擷取您的最愛。</li>\n</ul>\n</li>\n<li><b>🖼️ 最愛的藝術家按鈕：</b>\n<ul>\n<li>點擊此處可開啟一個對話方塊，列出您在 Kemono.su 上收藏的所有藝術家。</li>\n<li>您可以從此列表中選擇一位或多位藝術家來下載他們的內容。</li>\n</ul>\n</li>\n<li><b>📄 最愛的貼文按鈕（未來功能）：</b>\n<ul>\n<li>下載特定收藏的<i>貼文</i>（特別是如果它們是系列的一部分，則以類似漫畫的循序順序）是一項目前正在開發的功能。</li>\n<li>處理收藏貼文的最佳方式，特別是對於像漫畫這樣的循序閱讀，仍在探索中。</li>\n<li>如果您對於如何下載和組織收藏貼文有任何想法或特定用例（例如：從最愛中進行「漫畫風格」），請考慮在專案的 GitHub 頁面上提出問題或加入討論。您的意見非常寶貴！</li>\n</ul>\n</li>\n<li><b>最愛下載範圍（按鈕）：</b>\n<ul>\n<li>此按鈕（位於「最愛的貼文」旁邊）控制所選最愛藝術家內容的下載位置：\n<ul>\n<li><b><i>範圍：所選位置：</i></b>所有選定的藝術家都將下載到您在 UI 中設定的主要「下載位置」。篩選器會全域應用於所有內容。</li>\n<li><b><i>範圍：藝術家資料夾：</i></b>對於每位選定的藝術家，將在您的主要「下載位置」內自動建立一個子資料夾（以藝術家姓名命名）。該藝術家的內容將進入其特定資料夾。篩選器會在每個藝術家的專用資料夾內應用。</li>\n</ul>\n</li>\n</ul>\n</li>\n<li><b>最愛模式中的篩選器：</b>\n<ul>\n<li>您在 UI 中設定的「🎯 按角色篩選」、「🚫 使用關鍵字跳過」和「篩選檔案」選項仍將適用於從您選定的最愛藝術家下載的內容。</li>\n</ul>\n</li>\n</ul></body></html>",
"help_guide_step9_title":"⑨ 關鍵檔案與導覽",
"help_guide_step9_content":"<html><head/><body>\n<h3>應用程式使用的關鍵檔案</h3>\n<ul>\n<li><b><code>Known.txt</code>：</b>\n<ul>\n<li>位於應用程式目錄中（<code>.exe</code> 或 <code>main.py</code> 所在的位置）。</li>\n<li>在啟用「按名稱/標題分開資料夾」時，儲存您已知的節目、角色或系列標題列表，以便自動組織資料夾。</li>\n<li><b>格式：</b>\n<ul>\n<li>每一行都是一個條目。</li>\n<li><b>單一名稱：</b>例如：<code>我的精彩系列</code>。符合此內容的內容將進入名為「我的精彩系列」的資料夾。</li>\n<li><b>群組別名：</b>例如：<code>(角色 A, 角 A, 備用名稱 A)</code>。符合「角色 A」、「角 A」或「備用名稱 A」的內容都將進入一個名為「角色 A 角 A 備用名稱 A」的資料夾（經過清理）。括號中的所有術語都成為該資料夾的別名。</li>\n</ul>\n</li>\n<li><b>用途：</b>如果貼文不符合您目前作用中的「按角色篩選」輸入，則作為資料夾命名的備用選項。您可以透過 UI 管理簡單條目，或直接編輯檔案以處理複雜的別名。應用程式會在啟動或下次使用時重新載入它。</li>\n</ul>\n</li>\n<li><b><code>cookies.txt</code>（可選）：</b>\n<ul>\n<li>如果您使用「使用 Cookie」功能，且未提供直接的 cookie 字串或瀏覽特定檔案，應用程式將在其目錄中尋找名為 <code>cookies.txt</code> 的檔案。</li>\n<li><b>格式：</b>必須是 Netscape cookie 檔案格式。</li>\n<li><b>用途：</b>允許下載器使用您的瀏覽器登入工作階段來存取可能需要登入 Kemono/Coomer 的內容。</li>\n</ul>\n</li>\n</ul>\n<h3>首次使用者導覽</h3>\n<ul>\n<li>首次啟動時（或如果重設），會出現一個歡迎導覽對話方塊，引導您了解主要功能。您可以跳過它或選擇「不再顯示此導覽」。</li>\n</ul>\n<p><em>許多 UI 元素也有工具提示，當您將滑鼠懸停在它們上方時會出現，提供快速提示。</em></p>\n</body></html>"
})

def get_translation (language_code ,key ,default_text =""):
    """
    Retrieves a translation for a given key and language.
    Falls back to English if the key is not found in the specified language.
    Falls back to default_text if not found in English either or if the language_code itself is not found.
    """

    lang_translations =translations .get (language_code )
    if lang_translations and key in lang_translations :
        return lang_translations [key ]


    en_translations =translations .get ("en")
    if en_translations and key in en_translations :
        print (f"Warning: Translation key '{key }' not found for language '{language_code }'. Falling back to English.")
        return en_translations [key ]


    print (f"Warning: Translation key '{key }' not found for language '{language_code }' or English. Using default: '{default_text }'.")
    return default_text 
