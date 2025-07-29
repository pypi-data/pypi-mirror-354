# OutlookApp MCP Server

An MCP Server for the OutlookApp API.

## 🛠️ Tool List

This is automatically generated from OpenAPI schema for the OutlookApp API.


| Tool | Description |
|------|-------------|
| `get_user_inference_classification` | Retrieves inference classification data for a specific user, allowing optional selection and expansion of fields using query parameters. |
| `update_inference_classification_user` | Updates the inference classification details for a specific user using the PATCH method, applying partial modifications to the existing resource based on the provided JSON body. |
| `get_user_inference_overrides` | Retrieves and lists override classifications for a specific user using the provided parameters for filtering, sorting, and selecting data. |
| `override_user_inference` | Overrides inference classification settings for a specific user by sending a JSON payload with the updated override details. |
| `get_inference_override` | Retrieves details of a specific inference classification override for a user by ID, allowing optional selection and expansion of specific fields. |
| `patch_user_inference_override` | Updates specific properties of an inference classification override for a user using JSON Patch operations. |
| `delete_inference_override` | Deletes a specific inference classification override for a user using the provided user ID and inference classification override ID. |
| `count_user_inference_overrides` | Retrieves the count of inference classification overrides for a specified user ID using optional search and filter parameters. |
| `list_user_mail_folders` | Retrieves a list of mail folders for a specified user, allowing for optional filtering, sorting, and expansion of results. |
| `create_mail_folder` | Creates a new mail folder for a specified user using the provided JSON body and returns a relevant status response. |
| `get_mail_folder_details` | Retrieves information about a specific mail folder for a user, optionally including hidden folders and allowing selective expansion of related data. |
| `update_mail_folder` | Updates a specific mail folder for a user by applying partial modifications using a JSON request body. |
| `delete_mail_folder` | Deletes a specific mail folder for a user using the "DELETE" method, requiring the user ID and mail folder ID as path parameters and an "If-Match" header for optimistic concurrency control. |
| `list_child_folders` | Retrieves a list of child folders for a specified mail folder of a user using the "GET" method, allowing optional filtering and sorting through query parameters. |
| `create_child_folder` | Creates a new child folder within a specified mail folder for a given user using the provided JSON request body. |
| `get_mail_folder_childs` | Retrieves a list of child folders within a specified mail folder for a given user, allowing optional filtering by hidden folders and selection of specific fields. |
| `update_mail_folder_children` | Updates the properties of a child mail folder within a specified mail folder for a given user using the PATCH method. |
| `delete_child_folder` | Deletes a child mail folder from a specified mail folder for a given user. |
| `list_message_rules_in_child_folder` | Retrieves message rules for a child folder in a specific mail folder of a user, supporting filtering, sorting, and optional expansion of related data. |
| `create_message_rule_in_subfolder` | Creates a message rule in a specific child folder of a user's mailbox by specifying conditions and actions to be applied to incoming messages. |
| `get_nested_message_rules` | Retrieves a specific message rule in a mail folder, allowing optional selection and expansion of properties. |
| `update_message_rule` | Updates a specific message rule for a given mail folder of a user using a JSON body with operations to modify its properties. |
| `delete_message_rule` | Deletes a specific message rule for a user's mail folder using the DELETE method. |
| `count_message_rules` | Returns the total count of message rules for a specified mail folder belonging to a given user. |
| `list_user_mail_folder_messages` | Retrieves a list of messages from a specific mail folder belonging to a user, allowing for filtering, sorting, and selecting specific fields. |
| `create_child_folder_messages` | Creates a new message in a specified child mail folder of a user's mail folder using the provided JSON body. |
| `get_nested_message` | Retrieves a specific message from a child folder within a mail folder associated with a user's mailbox, allowing optional selection and expansion of properties. |
| `update_message_in_folder` | Modifies a specific email message in a nested mail folder using the PATCH method, updating properties as specified in the JSON request body. |
| `delete_message_by_id` | Deletes a specific message for a user using the provided user ID and message ID, potentially requiring an If-Match header for conditional requests. |
| `get_message_value` | Retrieves the content of a specific email message from a designated mail folder for a user. |
| `update_user_message` | Updates a specific message for a user using the provided JSON Patch operations and returns a status message based on the outcome. |
| `delete_message_by_user_and_folder_id` | Deletes a message from a specific folder within a user's mailbox using the DELETE method, requiring the user ID, mail folder IDs, and message ID, and optionally an If-Match header for concurrency control. |
| `get_mail_attachment` | Retrieves an attachment from a specific message in a child folder of a mail folder belonging to a user, optionally allowing filtering, sorting, and selecting specific properties. |
| `add_attachment_to_message` | Adds an attachment to a specific message in a mail folder using the provided JSON payload. |
| `get_attachment_details` | Retrieves a specific attachment from a message in a nested mail folder using the "GET" method, allowing optional filtering with `$select` and `$expand` parameters. |
| `delete_attachment` | Deletes an attachment from a message in a child folder of a mail folder belonging to a user using the DELETE method, requiring the user ID, mail folder IDs, message ID, and attachment ID. |
| `count_attachments` | Retrieves the count of attachments for a specific message in a nested mail folder using the "GET" method. |
| `create_upload_session` | Creates an upload session to allow attaching a file to a specific message located within a nested mail folder for a user using Microsoft Graph. |
| `get_extensions_by_message_id` | Retrieves and returns extensions for a specific message in a mail folder, allowing for optional filtering, sorting, and expansion of related data. |
| `add_message_extension` | Adds an extension to a specific message in a mail folder using the provided JSON payload. |
| `get_mail_message_extension` | Retrieves the specified extension for a message in a child folder of a mail folder belonging to a user, allowing for optional selection and expansion of specific properties. |
| `update_message_extension` | Updates an extension for a specific message in a mail folder of a user using the PATCH method, with the request body specifying the modifications to apply. |
| `delete_message_extension` | Deletes an extension from a specific message in a mail folder for a given user. |
| `get_extensions_count` | Retrieves the count of message extensions for a specific message in a mail folder belonging to a user. |
| `copy_message` | Copies a message to a folder within the specified user's mailbox using the Microsoft Graph API. |
| `create_message_forward` | Creates a draft to forward an existing message using the Microsoft Graph API, allowing specification of recipients and content in JSON or MIME format. |
| `create_reply_to_child_message` | Creates a draft message to reply to an existing email in a user's mailbox, using either JSON or MIME format, and requires specifying the user ID, mail folder IDs, and the message ID to be replied to. |
| `create_reply_all_message` | Creates a draft reply message addressed to the sender and all recipients of the specified message, supporting JSON or MIME format in the request body[1][4]. |
| `forward_message` | Forwards an email message using the Microsoft Graph API by specifying the user ID, mail folder ID, and message ID in the path, and providing the recipient details in the request body. |
| `move_message_to_folder` | Moves a message from a specified folder to another folder within the same user's mailbox by creating a new copy of the message in the destination folder and removing the original. |
| `delete_message_permanently` | Permanently deletes a message in a user's mailbox and moves it to the Purges folder using the Microsoft Graph API. |
| `reply_to_message_by_user` | Replies to an email message using the Microsoft Graph API by sending a response from a specific user's mailbox, maintaining the conversation thread. |
| `reply_all_to_message` | Sends a reply to all recipients of the specified message and saves it in the Sent Items folder[1][4]. |
| `send_user_message` | Sends a specified message using the Microsoft Graph API. |
| `count_user_mail_messages` | Retrieves the count of messages within a specific child folder of a user's mail folder using the "GET" method. |
| `get_delta_messages` | Tracks changes to messages in a specified mail folder of a user using the Microsoft Graph delta query, allowing retrieval of created, updated, or deleted messages based on optional query parameters such as change type. |
| `copy_child_folders` | Copies a child mail folder and its contents to another mail folder within a user's mailbox using the Microsoft Graph API. |
| `move_child_folder` | Moves a mail folder and its contents to another mail folder using the Microsoft Graph API. |
| `permanent_delete_child_folder` | Permanently deletes a mail folder and its child folder, removing all items from the user's mailbox using the Microsoft Graph API. |
| `get_child_folder_count` | Retrieves the count of child folders within a specified mail folder for a user. |
| `get_delta_child_folders` | Retrieves changes to child folders under a specified mail folder for a user using delta query, allowing applications to track newly created, updated, or deleted child folders without performing a full read of the data. |
| `list_user_mail_folder_message_rules` | Retrieves a list of message rules for a specified user and mail folder, supporting optional query parameters for filtering, sorting, and pagination. |
| `create_message_rule` | Creates a new message rule for a specific mail folder belonging to a user using the provided request body. |
| `get_message_rule_details` | Retrieves a specific message rule for a user’s mail folder using the provided user, mail folder, and rule identifiers. |
| `update_message_rule` | Updates a specific message rule for a given mail folder of a user using a JSON body with operations to modify its properties. |
| `delete_message_rule` | Deletes a specific message rule for a user's mail folder using the DELETE method. |
| `count_message_rules` | Returns the total count of message rules for a specified mail folder belonging to a given user. |
| `list_user_mail_folder_messages` | Retrieves a list of messages from a specific mail folder belonging to a user, allowing for filtering, sorting, and selecting specific fields. |
| `create_message_in_folder` | Creates a new message in the specified mail folder for the given user. |
| `get_user_mail_folder_message_by_id` | Retrieves a specific message from a user's mail folder using the provided user ID, mail folder ID, and message ID, optionally selecting specific fields and expanding related data. |
| `update_message_by_id` | Updates a specific email message in a given mail folder for a user, using JSON Patch operations to modify its properties. |
| `delete_message_by_id` | Deletes a specific message for a user using the provided user ID and message ID, potentially requiring an If-Match header for conditional requests. |
| `get_message_value` | Retrieves the content of a specific email message from a designated mail folder for a user. |
| `update_message_value` | Updates or replaces the content of a specific email message in a user's mailbox using the provided binary data. |
| `delete_message_content_by_id` | Deletes a message from a user's mail folder using the specified message ID, requiring the user ID and mail folder ID for identification. |
| `get_attachment_by_id` | Retrieves a specific attachment from a message associated with a user, allowing optional selection and expansion of fields through query parameters. |
| `add_attachment_to_message` | Adds an attachment to a specific message in a mail folder using the provided JSON payload. |
| `get_attachment_by_id` | Retrieves a specific attachment from a message associated with a user, allowing optional selection and expansion of fields through query parameters. |
| `delete_user_message_attachment` | Deletes an attachment from a specific message in a mail folder of a user, using the specified user ID, mail folder ID, message ID, and attachment ID. |
| `count_attachment_by_message_id` | Retrieves the total number of email attachments for a specified message in a user’s mail folder. |
| `create_message_attachment_upload_session` | Creates an upload session to iteratively upload ranges of a file as an attachment to a specified email message in the user's mailbox. |
| `get_extensions_by_message_id` | Retrieves and returns extensions for a specific message in a mail folder, allowing for optional filtering, sorting, and expansion of related data. |
| `add_message_extension` | Adds an extension to a specific message in a mail folder using the provided JSON payload. |
| `get_mail_extension` | Retrieves a specific extension for a message within a mail folder of a user, allowing optional selection and expansion of properties through query parameters. |
| `update_message_extension` | Updates an extension for a specific message in a mail folder of a user using the PATCH method, with the request body specifying the modifications to apply. |
| `delete_message_extension` | Deletes an extension from a specific message in a mail folder for a given user. |
| `get_extensions_count` | Retrieves the count of message extensions for a specific message in a mail folder belonging to a user. |
| `copy_message_to_folder` | Copies a message to a specified folder within a user's mailbox using the Microsoft Graph API. |
| `forward_message` | Forwards an email message using the Microsoft Graph API by specifying the user ID, mail folder ID, and message ID in the path, and providing the recipient details in the request body. |
| `create_reply_to_message` | Creates a draft message in JSON format to reply to an existing message using the Microsoft Graph API, allowing the specification of the reply content in the request body. |
| `create_reply_all_message` | Creates a draft reply message addressed to the sender and all recipients of the specified message, supporting JSON or MIME format in the request body[1][4]. |
| `forward_message` | Forwards an email message using the Microsoft Graph API by specifying the user ID, mail folder ID, and message ID in the path, and providing the recipient details in the request body. |
| `move_message_to_folder` | Moves a message from a specified folder to another folder within the same user's mailbox by creating a new copy of the message in the destination folder and removing the original. |
| `delete_message_permanently` | Permanently deletes a message in a user's mailbox and moves it to the Purges folder using the Microsoft Graph API. |
| `reply_message_by_id` | Replies to an email message using the Microsoft Graph API, specifying the user ID, mail folder ID, and message ID, and requiring a JSON body in the request. |
| `reply_all_message` | Replies to all recipients of a specified email message using the Microsoft Graph API, creating and sending the reply in a single call. |
| `send_user_message` | Sends a specified message using the Microsoft Graph API. |
| `count_user_mail_folder_messages` | Retrieves the count of messages in a specified mail folder for a given user using the GET method. |
| `get_delta_messages` | Tracks changes to messages in a specified mail folder of a user using the Microsoft Graph delta query, allowing retrieval of created, updated, or deleted messages based on optional query parameters such as change type. |
| `copy_mail_folder` | Copies a specified mail folder and its contents to another mail folder for a given user using the Microsoft Graph API. |
| `move_mail_folder` | Moves a mail folder and its contents to another mail folder using the Microsoft Graph API. |
| `permanently_delete_mail_folder` | Permanently deletes a specified mail folder and its items from a user's mailbox using the Microsoft Graph API. |
| `get_mail_folder_count` | Retrieves the count of mail folders for a specified user using the provided search and filter parameters. |
| `list_user_mail_folders_delta` | Tracks changes to mail folders for a specified user using the delta function, allowing applications to discover newly created, updated, or deleted entities without performing a full read. |
| `list_user_messages` | Retrieves a list of messages for a specified user, allowing optional filtering and sorting with query parameters such as includeHiddenMessages, top, skip, search, filter, count, orderby, select, and expand. |
| `create_user_message` | Sends a message to a specified user using their ID and returns a status message. |
| `get_message_details` | Retrieves a specific message identified by `{message-id}` for a user with `{user-id}`, allowing optional filtering with `includeHiddenMessages`, selection of specific fields with `$select`, and expansion of related data with `$expand`. |
| `update_user_message` | Updates a specific message for a user using the provided JSON Patch operations and returns a status message based on the outcome. |
| `delete_user_message_by_id` | Deletes a specific message identified by `message-id` for a user with the specified `user-id`, returning a successful status if the operation is completed. |
| `get_user_message_value_raw` | Retrieves the raw value of a specific message for a specified user. |
| `update_user_message_value` | Updates the content of a specific message identified by `{message-id}` for a user with `{user-id}` using a binary payload. |
| `delete_message_by_id` | Deletes a specific message for a user using the provided user ID and message ID, potentially requiring an If-Match header for conditional requests. |
| `get_attachment_by_user_message_id` | Retrieves attachments for a specific message belonging to a user, with optional filtering and sorting capabilities. |
| `add_user_message_attachment` | Adds a new attachment to a specific message for a user using the provided JSON payload. |
| `get_attachment_by_id` | Retrieves a specific attachment from a message associated with a user, allowing optional selection and expansion of fields through query parameters. |
| `delete_attachment_by_id` | Deletes an attachment from a specific message belonging to a user using the provided IDs and returns a status message, optionally requiring an "If-Match" header for version control. |
| `get_attachment_count` | Retrieves the number of attachments for a specific message of a user using the GET method. |
| `create_upload_session_for_message` | Creates an upload session to iteratively upload a file as an attachment to a specified Outlook message, returning an upload URL for subsequent file upload operations. |
| `get_extensions_for_message` | Retrieves message extensions for a specific message belonging to a user, allowing for optional filtering, sorting, and selection of fields. |
| `create_message_extension` | Adds an extension to a specific message for a given user using the provided JSON data. |
| `get_extension_details` | Retrieves details about a specific extension for a message associated with a user, allowing optional filtering and expansion of the response using query parameters. |
| `patch_user_message_extension_by_id` | Updates specific properties of an extension within a message for a specified user using the PATCH method, requiring a JSON body with the changes. |
| `delete_extension_by_user_message_id` | Deletes a specific extension from a message identified by its ID associated with a user, using the "DELETE" method. |
| `count_message_extension` | Retrieves the count of message extensions for a specified message owned by a specific user, optionally filtered or searched according to query parameters. |
| `copy_message` | Copies a message to a folder within the specified user's mailbox using the Microsoft Graph API. |
| `forward_message_by_user` | Creates a draft to forward an existing message, allowing specification of recipients and content in either JSON or MIME format, which can be updated and sent in a subsequent operation. |
| `create_reply_to_message` | Creates a draft message in JSON format to reply to an existing message using the Microsoft Graph API, allowing the specification of the reply content in the request body. |
| `create_reply_all_message` | Creates a draft reply message addressed to the sender and all recipients of the specified message, supporting JSON or MIME format in the request body[1][4]. |
| `forward_message_by_id` | Forwards an email message using the Microsoft Graph API by specifying the recipient and optionally adding a comment, saving the forwarded message in the Sent Items folder. |
| `move_user_message` | Moves a message to another folder within the specified user's mailbox by creating a new copy of the message in the destination folder. |
| `delete_message_permanently` | Permanently deletes a message in a user's mailbox and moves it to the Purges folder using the Microsoft Graph API. |
| `reply_message` | Replies to an email message using the Microsoft Graph API by sending a response to the original message based on the provided message ID and user ID. |
| `reply_all_user_message_by_id` | Sends a reply to all recipients of a specified message using the Microsoft Graph API, creating and sending the email in a single call. |
| `send_user_message` | Sends a specified message using the Microsoft Graph API. |
| `count_user_messages` | Retrieves the count of messages for a specific user, using the provided user ID and optionally applying search and filter parameters. |
| `get_microsoft_graph_delta_messages_by_user_id` | Tracks changes in messages for a specific user using the Microsoft Graph API, allowing retrieval of newly created, updated, or deleted messages based on optional query parameters such as change type and filtering options. |
