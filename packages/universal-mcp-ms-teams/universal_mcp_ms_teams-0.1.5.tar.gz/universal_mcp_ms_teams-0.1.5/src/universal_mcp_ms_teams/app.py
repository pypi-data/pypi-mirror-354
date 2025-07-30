from typing import Any, Optional, List
from universal_mcp.applications import APIApplication
from universal_mcp.integrations import Integration

class MsTeamsApp(APIApplication):
    def __init__(self, integration: Integration = None, **kwargs) -> None:
        super().__init__(name='ms-teams', integration=integration, **kwargs)
        self.base_url = "https://graph.microsoft.com/v1.0"

    def list_teams(self, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        List teams

        Args:
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.team, important
        """
        url = f"{self.base_url}/teams"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def create_team(self, id: Optional[str] = None, classification: Optional[str] = None, createdDateTime: Optional[str] = None, description: Optional[str] = None, displayName: Optional[str] = None, firstChannelName: Optional[str] = None, funSettings: Optional[dict[str, dict[str, Any]]] = None, guestSettings: Optional[dict[str, dict[str, Any]]] = None, internalId: Optional[str] = None, isArchived: Optional[bool] = None, memberSettings: Optional[dict[str, dict[str, Any]]] = None, messagingSettings: Optional[dict[str, dict[str, Any]]] = None, specialization: Optional[str] = None, summary: Optional[dict[str, dict[str, Any]]] = None, tenantId: Optional[str] = None, visibility: Optional[str] = None, webUrl: Optional[str] = None, allChannels: Optional[List[Any]] = None, channels: Optional[List[Any]] = None, group: Optional[Any] = None, incomingChannels: Optional[List[Any]] = None, installedApps: Optional[List[Any]] = None, members: Optional[List[Any]] = None, operations: Optional[List[Any]] = None, permissionGrants: Optional[List[Any]] = None, photo: Optional[Any] = None, primaryChannel: Optional[Any] = None, schedule: Optional[Any] = None, tags: Optional[List[Any]] = None, template: Optional[Any] = None) -> Any:
        """
        Create team

        Args:
            id (string): The unique identifier for an entity. Read-only.
            classification (string): An optional label. Typically describes the data or business sensitivity of the team. Must match one of a preconfigured set in the tenant's directory.
            createdDateTime (string): Timestamp at which the team was created.
            description (string): An optional description for the team. Maximum length: 1,024 characters.
            displayName (string): The name of the team.
            firstChannelName (string): The name of the first channel in the team. This is an optional property, only used during team creation and isn't returned in methods to get and list teams.
            funSettings (object): funSettings
            guestSettings (object): guestSettings
            internalId (string): A unique ID for the team that was used in a few places such as the audit log/Office 365 Management Activity API.
            isArchived (boolean): Whether this team is in read-only mode.
            memberSettings (object): memberSettings
            messagingSettings (object): messagingSettings
            specialization (string): specialization
            summary (object): summary
            tenantId (string): The ID of the Microsoft Entra tenant.
            visibility (string): visibility
            webUrl (string): A hyperlink that goes to the team in the Microsoft Teams client. You get this URL when you right-click a team in the Microsoft Teams client and select Get link to team. This URL should be treated as an opaque blob, and not parsed.
            allChannels (array): List of channels either hosted in or shared with the team (incoming channels).
            channels (array): The collection of channels and messages associated with the team.
            group (string): group
            incomingChannels (array): List of channels shared with the team.
            installedApps (array): The apps installed in this team.
            members (array): Members and owners of the team.
            operations (array): The async operations that ran or are running on this team.
            permissionGrants (array): A collection of permissions granted to apps to access the team.
            photo (string): photo
            primaryChannel (string): primaryChannel
            schedule (string): schedule
            tags (array): The tags associated with the team.
            template (string): template

        Returns:
            Any: Created entity

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.team, important
        """
        request_body_data = None
        request_body_data = {
            'id': id,
            'classification': classification,
            'createdDateTime': createdDateTime,
            'description': description,
            'displayName': displayName,
            'firstChannelName': firstChannelName,
            'funSettings': funSettings,
            'guestSettings': guestSettings,
            'internalId': internalId,
            'isArchived': isArchived,
            'memberSettings': memberSettings,
            'messagingSettings': messagingSettings,
            'specialization': specialization,
            'summary': summary,
            'tenantId': tenantId,
            'visibility': visibility,
            'webUrl': webUrl,
            'allChannels': allChannels,
            'channels': channels,
            'group': group,
            'incomingChannels': incomingChannels,
            'installedApps': installedApps,
            'members': members,
            'operations': operations,
            'permissionGrants': permissionGrants,
            'photo': photo,
            'primaryChannel': primaryChannel,
            'schedule': schedule,
            'tags': tags,
            'template': template,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def get_team_info(self, team_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get team

        Args:
            team_id (string): team-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved entity

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.team, important
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        url = f"{self.base_url}/teams/{team_id}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_team(self, team_id: str, id: Optional[str] = None, classification: Optional[str] = None, createdDateTime: Optional[str] = None, description: Optional[str] = None, displayName: Optional[str] = None, firstChannelName: Optional[str] = None, funSettings: Optional[dict[str, dict[str, Any]]] = None, guestSettings: Optional[dict[str, dict[str, Any]]] = None, internalId: Optional[str] = None, isArchived: Optional[bool] = None, memberSettings: Optional[dict[str, dict[str, Any]]] = None, messagingSettings: Optional[dict[str, dict[str, Any]]] = None, specialization: Optional[str] = None, summary: Optional[dict[str, dict[str, Any]]] = None, tenantId: Optional[str] = None, visibility: Optional[str] = None, webUrl: Optional[str] = None, allChannels: Optional[List[Any]] = None, channels: Optional[List[Any]] = None, group: Optional[Any] = None, incomingChannels: Optional[List[Any]] = None, installedApps: Optional[List[Any]] = None, members: Optional[List[Any]] = None, operations: Optional[List[Any]] = None, permissionGrants: Optional[List[Any]] = None, photo: Optional[Any] = None, primaryChannel: Optional[Any] = None, schedule: Optional[Any] = None, tags: Optional[List[Any]] = None, template: Optional[Any] = None) -> Any:
        """
        Update team

        Args:
            team_id (string): team-id
            id (string): The unique identifier for an entity. Read-only.
            classification (string): An optional label. Typically describes the data or business sensitivity of the team. Must match one of a preconfigured set in the tenant's directory.
            createdDateTime (string): Timestamp at which the team was created.
            description (string): An optional description for the team. Maximum length: 1,024 characters.
            displayName (string): The name of the team.
            firstChannelName (string): The name of the first channel in the team. This is an optional property, only used during team creation and isn't returned in methods to get and list teams.
            funSettings (object): funSettings
            guestSettings (object): guestSettings
            internalId (string): A unique ID for the team that was used in a few places such as the audit log/Office 365 Management Activity API.
            isArchived (boolean): Whether this team is in read-only mode.
            memberSettings (object): memberSettings
            messagingSettings (object): messagingSettings
            specialization (string): specialization
            summary (object): summary
            tenantId (string): The ID of the Microsoft Entra tenant.
            visibility (string): visibility
            webUrl (string): A hyperlink that goes to the team in the Microsoft Teams client. You get this URL when you right-click a team in the Microsoft Teams client and select Get link to team. This URL should be treated as an opaque blob, and not parsed.
            allChannels (array): List of channels either hosted in or shared with the team (incoming channels).
            channels (array): The collection of channels and messages associated with the team.
            group (string): group
            incomingChannels (array): List of channels shared with the team.
            installedApps (array): The apps installed in this team.
            members (array): Members and owners of the team.
            operations (array): The async operations that ran or are running on this team.
            permissionGrants (array): A collection of permissions granted to apps to access the team.
            photo (string): photo
            primaryChannel (string): primaryChannel
            schedule (string): schedule
            tags (array): The tags associated with the team.
            template (string): template

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.team
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'classification': classification,
            'createdDateTime': createdDateTime,
            'description': description,
            'displayName': displayName,
            'firstChannelName': firstChannelName,
            'funSettings': funSettings,
            'guestSettings': guestSettings,
            'internalId': internalId,
            'isArchived': isArchived,
            'memberSettings': memberSettings,
            'messagingSettings': messagingSettings,
            'specialization': specialization,
            'summary': summary,
            'tenantId': tenantId,
            'visibility': visibility,
            'webUrl': webUrl,
            'allChannels': allChannels,
            'channels': channels,
            'group': group,
            'incomingChannels': incomingChannels,
            'installedApps': installedApps,
            'members': members,
            'operations': operations,
            'permissionGrants': permissionGrants,
            'photo': photo,
            'primaryChannel': primaryChannel,
            'schedule': schedule,
            'tags': tags,
            'template': template,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams/{team_id}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def delete_team_entity(self, team_id: str) -> Any:
        """
        Delete entity from teams

        Args:
            team_id (string): team-id

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.team
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        url = f"{self.base_url}/teams/{team_id}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def list_channels_for_team(self, team_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        List channels

        Args:
            team_id (string): team-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel, important
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def create_team_channel(self, team_id: str, id: Optional[str] = None, createdDateTime: Optional[str] = None, description: Optional[str] = None, displayName: Optional[str] = None, email: Optional[str] = None, isArchived: Optional[bool] = None, isFavoriteByDefault: Optional[bool] = None, membershipType: Optional[str] = None, summary: Optional[dict[str, dict[str, Any]]] = None, tenantId: Optional[str] = None, webUrl: Optional[str] = None, allMembers: Optional[List[Any]] = None, filesFolder: Optional[Any] = None, members: Optional[List[Any]] = None, messages: Optional[List[Any]] = None, sharedWithTeams: Optional[List[Any]] = None, tabs: Optional[List[Any]] = None) -> Any:
        """
        Create channel

        Args:
            team_id (string): team-id
            id (string): The unique identifier for an entity. Read-only.
            createdDateTime (string): Read only. Timestamp at which the channel was created.
            description (string): Optional textual description for the channel.
            displayName (string): Channel name as it will appear to the user in Microsoft Teams. The maximum length is 50 characters.
            email (string): The email address for sending messages to the channel. Read-only.
            isArchived (boolean): Indicates whether the channel is archived. Read-only.
            isFavoriteByDefault (boolean): Indicates whether the channel should be marked as recommended for all members of the team to show in their channel list. Note: All recommended channels automatically show in the channels list for education and frontline worker users. The property can only be set programmatically via the Create team method. The default value is false.
            membershipType (string): membershipType
            summary (object): summary
            tenantId (string): The ID of the Microsoft Entra tenant.
            webUrl (string): A hyperlink that will go to the channel in Microsoft Teams. This is the URL that you get when you right-click a channel in Microsoft Teams and select Get link to channel. This URL should be treated as an opaque blob, and not parsed. Read-only.
            allMembers (array): A collection of membership records associated with the channel, including both direct and indirect members of shared channels.
            filesFolder (string): filesFolder
            members (array): A collection of membership records associated with the channel.
            messages (array): A collection of all the messages in the channel. A navigation property. Nullable.
            sharedWithTeams (array): A collection of teams with which a channel is shared.
            tabs (array): A collection of all the tabs in the channel. A navigation property.

        Returns:
            Any: Created navigation property.

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel, important
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'createdDateTime': createdDateTime,
            'description': description,
            'displayName': displayName,
            'email': email,
            'isArchived': isArchived,
            'isFavoriteByDefault': isFavoriteByDefault,
            'membershipType': membershipType,
            'summary': summary,
            'tenantId': tenantId,
            'webUrl': webUrl,
            'allMembers': allMembers,
            'filesFolder': filesFolder,
            'members': members,
            'messages': messages,
            'sharedWithTeams': sharedWithTeams,
            'tabs': tabs,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams/{team_id}/channels"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def get_team_channel_info(self, team_id: str, channel_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get channel

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_channel(self, team_id: str, channel_id: str, id: Optional[str] = None, createdDateTime: Optional[str] = None, description: Optional[str] = None, displayName: Optional[str] = None, email: Optional[str] = None, isArchived: Optional[bool] = None, isFavoriteByDefault: Optional[bool] = None, membershipType: Optional[str] = None, summary: Optional[dict[str, dict[str, Any]]] = None, tenantId: Optional[str] = None, webUrl: Optional[str] = None, allMembers: Optional[List[Any]] = None, filesFolder: Optional[Any] = None, members: Optional[List[Any]] = None, messages: Optional[List[Any]] = None, sharedWithTeams: Optional[List[Any]] = None, tabs: Optional[List[Any]] = None) -> Any:
        """
        Patch channel

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            id (string): The unique identifier for an entity. Read-only.
            createdDateTime (string): Read only. Timestamp at which the channel was created.
            description (string): Optional textual description for the channel.
            displayName (string): Channel name as it will appear to the user in Microsoft Teams. The maximum length is 50 characters.
            email (string): The email address for sending messages to the channel. Read-only.
            isArchived (boolean): Indicates whether the channel is archived. Read-only.
            isFavoriteByDefault (boolean): Indicates whether the channel should be marked as recommended for all members of the team to show in their channel list. Note: All recommended channels automatically show in the channels list for education and frontline worker users. The property can only be set programmatically via the Create team method. The default value is false.
            membershipType (string): membershipType
            summary (object): summary
            tenantId (string): The ID of the Microsoft Entra tenant.
            webUrl (string): A hyperlink that will go to the channel in Microsoft Teams. This is the URL that you get when you right-click a channel in Microsoft Teams and select Get link to channel. This URL should be treated as an opaque blob, and not parsed. Read-only.
            allMembers (array): A collection of membership records associated with the channel, including both direct and indirect members of shared channels.
            filesFolder (string): filesFolder
            members (array): A collection of membership records associated with the channel.
            messages (array): A collection of all the messages in the channel. A navigation property. Nullable.
            sharedWithTeams (array): A collection of teams with which a channel is shared.
            tabs (array): A collection of all the tabs in the channel. A navigation property.

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'createdDateTime': createdDateTime,
            'description': description,
            'displayName': displayName,
            'email': email,
            'isArchived': isArchived,
            'isFavoriteByDefault': isFavoriteByDefault,
            'membershipType': membershipType,
            'summary': summary,
            'tenantId': tenantId,
            'webUrl': webUrl,
            'allMembers': allMembers,
            'filesFolder': filesFolder,
            'members': members,
            'messages': messages,
            'sharedWithTeams': sharedWithTeams,
            'tabs': tabs,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def delete_channel(self, team_id: str, channel_id: str) -> Any:
        """
        Delete channel

        Args:
            team_id (string): team-id
            channel_id (string): channel-id

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def get_team_members_list(self, team_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        List members of team

        Args:
            team_id (string): team-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.conversationMember, important
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        url = f"{self.base_url}/teams/{team_id}/members"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def add_member_to_team(self, team_id: str, id: Optional[str] = None, displayName: Optional[str] = None, roles: Optional[List[str]] = None, visibleHistoryStartDateTime: Optional[str] = None) -> Any:
        """
        Add member to team

        Args:
            team_id (string): team-id
            id (string): The unique identifier for an entity. Read-only.
            displayName (string): The display name of the user.
            roles (array): The roles for that user. This property contains more qualifiers only when relevant - for example, if the member has owner privileges, the roles property contains owner as one of the values. Similarly, if the member is an in-tenant guest, the roles property contains guest as one of the values. A basic member shouldn't have any values specified in the roles property. An Out-of-tenant external member is assigned the owner role.
            visibleHistoryStartDateTime (string): The timestamp denoting how far back a conversation's history is shared with the conversation member. This property is settable only for members of a chat.

        Returns:
            Any: Created navigation property.

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.conversationMember, important
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'displayName': displayName,
            'roles': roles,
            'visibleHistoryStartDateTime': visibleHistoryStartDateTime,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams/{team_id}/members"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def list_channel_messages_by_id(self, team_id: str, channel_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        List channel messages

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel, important
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/messages"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def send_chat_message(self, team_id: str, channel_id: str, id: Optional[str] = None, attachments: Optional[List[dict[str, dict[str, Any]]]] = None, body: Optional[dict[str, dict[str, Any]]] = None, channelIdentity: Optional[dict[str, dict[str, Any]]] = None, chatId: Optional[str] = None, createdDateTime: Optional[str] = None, deletedDateTime: Optional[str] = None, etag: Optional[str] = None, eventDetail: Optional[dict[str, dict[str, Any]]] = None, from_: Optional[Any] = None, importance: Optional[str] = None, lastEditedDateTime: Optional[str] = None, lastModifiedDateTime: Optional[str] = None, locale: Optional[str] = None, mentions: Optional[List[dict[str, dict[str, Any]]]] = None, messageHistory: Optional[List[dict[str, dict[str, Any]]]] = None, messageType: Optional[str] = None, policyViolation: Optional[dict[str, dict[str, Any]]] = None, reactions: Optional[List[dict[str, dict[str, Any]]]] = None, replyToId: Optional[str] = None, subject: Optional[str] = None, summary: Optional[str] = None, webUrl: Optional[str] = None, hostedContents: Optional[List[Any]] = None, replies: Optional[List[Any]] = None) -> Any:
        """
        Send chatMessage in a channel or a chat

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            id (string): The unique identifier for an entity. Read-only.
            attachments (array): References to attached objects like files, tabs, meetings etc.
            body (object): body
            channelIdentity (object): channelIdentity
            chatId (string): If the message was sent in a chat, represents the identity of the chat.
            createdDateTime (string): Timestamp of when the chat message was created.
            deletedDateTime (string): Read only. Timestamp at which the chat message was deleted, or null if not deleted.
            etag (string): Read-only. Version number of the chat message.
            eventDetail (object): eventDetail
            from_ (string): from
            importance (string): importance
            lastEditedDateTime (string): Read only. Timestamp when edits to the chat message were made. Triggers an 'Edited' flag in the Teams UI. If no edits are made the value is null.
            lastModifiedDateTime (string): Read only. Timestamp when the chat message is created (initial setting) or modified, including when a reaction is added or removed.
            locale (string): Locale of the chat message set by the client. Always set to en-us.
            mentions (array): List of entities mentioned in the chat message. Supported entities are: user, bot, team, channel, chat, and tag.
            messageHistory (array): List of activity history of a message item, including modification time and actions, such as reactionAdded, reactionRemoved, or reaction changes, on the message.
            messageType (string): messageType
            policyViolation (object): policyViolation
            reactions (array): Reactions for this chat message (for example, Like).
            replyToId (string): Read-only. ID of the parent chat message or root chat message of the thread. (Only applies to chat messages in channels, not chats.)
            subject (string): The subject of the chat message, in plaintext.
            summary (string): Summary text of the chat message that could be used for push notifications and summary views or fall back views. Only applies to channel chat messages, not chat messages in a chat.
            webUrl (string): Read-only. Link to the message in Microsoft Teams.
            hostedContents (array): Content in a message hosted by Microsoft Teams - for example, images or code snippets.
            replies (array): Replies for a specified message. Supports $expand for channel messages.

        Returns:
            Any: Created navigation property.

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel, important
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'attachments': attachments,
            'body': body,
            'channelIdentity': channelIdentity,
            'chatId': chatId,
            'createdDateTime': createdDateTime,
            'deletedDateTime': deletedDateTime,
            'etag': etag,
            'eventDetail': eventDetail,
            'from': from_,
            'importance': importance,
            'lastEditedDateTime': lastEditedDateTime,
            'lastModifiedDateTime': lastModifiedDateTime,
            'locale': locale,
            'mentions': mentions,
            'messageHistory': messageHistory,
            'messageType': messageType,
            'policyViolation': policyViolation,
            'reactions': reactions,
            'replyToId': replyToId,
            'subject': subject,
            'summary': summary,
            'webUrl': webUrl,
            'hostedContents': hostedContents,
            'replies': replies,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/messages"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def list_all_team_channel_members(self, team_id: str, channel_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        List allMembers

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/allMembers"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def create_team_channel_members(self, team_id: str, channel_id: str, id: Optional[str] = None, displayName: Optional[str] = None, roles: Optional[List[str]] = None, visibleHistoryStartDateTime: Optional[str] = None) -> Any:
        """
        Create new navigation property to allMembers for teams

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            id (string): The unique identifier for an entity. Read-only.
            displayName (string): The display name of the user.
            roles (array): The roles for that user. This property contains more qualifiers only when relevant - for example, if the member has owner privileges, the roles property contains owner as one of the values. Similarly, if the member is an in-tenant guest, the roles property contains guest as one of the values. A basic member shouldn't have any values specified in the roles property. An Out-of-tenant external member is assigned the owner role.
            visibleHistoryStartDateTime (string): The timestamp denoting how far back a conversation's history is shared with the conversation member. This property is settable only for members of a chat.

        Returns:
            Any: Created navigation property.

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'displayName': displayName,
            'roles': roles,
            'visibleHistoryStartDateTime': visibleHistoryStartDateTime,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/allMembers"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def get_team_channel_members_details(self, team_id: str, channel_id: str, conversationMember_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get allMembers from teams

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            conversationMember_id (string): conversationMember-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if conversationMember_id is None:
            raise ValueError("Missing required parameter 'conversationMember-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/allMembers/{conversationMember_id}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_conversation_member_in_team(self, team_id: str, channel_id: str, conversationMember_id: str, id: Optional[str] = None, displayName: Optional[str] = None, roles: Optional[List[str]] = None, visibleHistoryStartDateTime: Optional[str] = None) -> Any:
        """
        Update the navigation property allMembers in teams

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            conversationMember_id (string): conversationMember-id
            id (string): The unique identifier for an entity. Read-only.
            displayName (string): The display name of the user.
            roles (array): The roles for that user. This property contains more qualifiers only when relevant - for example, if the member has owner privileges, the roles property contains owner as one of the values. Similarly, if the member is an in-tenant guest, the roles property contains guest as one of the values. A basic member shouldn't have any values specified in the roles property. An Out-of-tenant external member is assigned the owner role.
            visibleHistoryStartDateTime (string): The timestamp denoting how far back a conversation's history is shared with the conversation member. This property is settable only for members of a chat.

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if conversationMember_id is None:
            raise ValueError("Missing required parameter 'conversationMember-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'displayName': displayName,
            'roles': roles,
            'visibleHistoryStartDateTime': visibleHistoryStartDateTime,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/allMembers/{conversationMember_id}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def delete_team_channel_member(self, team_id: str, channel_id: str, conversationMember_id: str) -> Any:
        """
        Delete navigation property allMembers for teams

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            conversationMember_id (string): conversationMember-id

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if conversationMember_id is None:
            raise ValueError("Missing required parameter 'conversationMember-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/allMembers/{conversationMember_id}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def list_channel_members_by_team_and_channel(self, team_id: str, channel_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        List members of a channel

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/members"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def add_member_to_channel_teamwise(self, team_id: str, channel_id: str, id: Optional[str] = None, displayName: Optional[str] = None, roles: Optional[List[str]] = None, visibleHistoryStartDateTime: Optional[str] = None) -> Any:
        """
        Add member to channel

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            id (string): The unique identifier for an entity. Read-only.
            displayName (string): The display name of the user.
            roles (array): The roles for that user. This property contains more qualifiers only when relevant - for example, if the member has owner privileges, the roles property contains owner as one of the values. Similarly, if the member is an in-tenant guest, the roles property contains guest as one of the values. A basic member shouldn't have any values specified in the roles property. An Out-of-tenant external member is assigned the owner role.
            visibleHistoryStartDateTime (string): The timestamp denoting how far back a conversation's history is shared with the conversation member. This property is settable only for members of a chat.

        Returns:
            Any: Created navigation property.

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'displayName': displayName,
            'roles': roles,
            'visibleHistoryStartDateTime': visibleHistoryStartDateTime,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/members"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def get_channel_member(self, team_id: str, channel_id: str, conversationMember_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get member of channel

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            conversationMember_id (string): conversationMember-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if conversationMember_id is None:
            raise ValueError("Missing required parameter 'conversationMember-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/members/{conversationMember_id}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_channel_member_by_id(self, team_id: str, channel_id: str, conversationMember_id: str, id: Optional[str] = None, displayName: Optional[str] = None, roles: Optional[List[str]] = None, visibleHistoryStartDateTime: Optional[str] = None) -> Any:
        """
        Update member in channel

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            conversationMember_id (string): conversationMember-id
            id (string): The unique identifier for an entity. Read-only.
            displayName (string): The display name of the user.
            roles (array): The roles for that user. This property contains more qualifiers only when relevant - for example, if the member has owner privileges, the roles property contains owner as one of the values. Similarly, if the member is an in-tenant guest, the roles property contains guest as one of the values. A basic member shouldn't have any values specified in the roles property. An Out-of-tenant external member is assigned the owner role.
            visibleHistoryStartDateTime (string): The timestamp denoting how far back a conversation's history is shared with the conversation member. This property is settable only for members of a chat.

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if conversationMember_id is None:
            raise ValueError("Missing required parameter 'conversationMember-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'displayName': displayName,
            'roles': roles,
            'visibleHistoryStartDateTime': visibleHistoryStartDateTime,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/members/{conversationMember_id}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def delete_conversation_member(self, team_id: str, channel_id: str, conversationMember_id: str) -> Any:
        """
        Delete conversationMember

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            conversationMember_id (string): conversationMember-id

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if conversationMember_id is None:
            raise ValueError("Missing required parameter 'conversationMember-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/members/{conversationMember_id}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def get_chat_message(self, team_id: str, channel_id: str, chatMessage_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get chatMessage in a channel or chat

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel, important
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/messages/{chatMessage_id}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_chat_message_by_team_channel(self, team_id: str, channel_id: str, chatMessage_id: str, id: Optional[str] = None, attachments: Optional[List[dict[str, dict[str, Any]]]] = None, body: Optional[dict[str, dict[str, Any]]] = None, channelIdentity: Optional[dict[str, dict[str, Any]]] = None, chatId: Optional[str] = None, createdDateTime: Optional[str] = None, deletedDateTime: Optional[str] = None, etag: Optional[str] = None, eventDetail: Optional[dict[str, dict[str, Any]]] = None, from_: Optional[Any] = None, importance: Optional[str] = None, lastEditedDateTime: Optional[str] = None, lastModifiedDateTime: Optional[str] = None, locale: Optional[str] = None, mentions: Optional[List[dict[str, dict[str, Any]]]] = None, messageHistory: Optional[List[dict[str, dict[str, Any]]]] = None, messageType: Optional[str] = None, policyViolation: Optional[dict[str, dict[str, Any]]] = None, reactions: Optional[List[dict[str, dict[str, Any]]]] = None, replyToId: Optional[str] = None, subject: Optional[str] = None, summary: Optional[str] = None, webUrl: Optional[str] = None, hostedContents: Optional[List[Any]] = None, replies: Optional[List[Any]] = None) -> Any:
        """
        Update chatMessage

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id
            id (string): The unique identifier for an entity. Read-only.
            attachments (array): References to attached objects like files, tabs, meetings etc.
            body (object): body
            channelIdentity (object): channelIdentity
            chatId (string): If the message was sent in a chat, represents the identity of the chat.
            createdDateTime (string): Timestamp of when the chat message was created.
            deletedDateTime (string): Read only. Timestamp at which the chat message was deleted, or null if not deleted.
            etag (string): Read-only. Version number of the chat message.
            eventDetail (object): eventDetail
            from_ (string): from
            importance (string): importance
            lastEditedDateTime (string): Read only. Timestamp when edits to the chat message were made. Triggers an 'Edited' flag in the Teams UI. If no edits are made the value is null.
            lastModifiedDateTime (string): Read only. Timestamp when the chat message is created (initial setting) or modified, including when a reaction is added or removed.
            locale (string): Locale of the chat message set by the client. Always set to en-us.
            mentions (array): List of entities mentioned in the chat message. Supported entities are: user, bot, team, channel, chat, and tag.
            messageHistory (array): List of activity history of a message item, including modification time and actions, such as reactionAdded, reactionRemoved, or reaction changes, on the message.
            messageType (string): messageType
            policyViolation (object): policyViolation
            reactions (array): Reactions for this chat message (for example, Like).
            replyToId (string): Read-only. ID of the parent chat message or root chat message of the thread. (Only applies to chat messages in channels, not chats.)
            subject (string): The subject of the chat message, in plaintext.
            summary (string): Summary text of the chat message that could be used for push notifications and summary views or fall back views. Only applies to channel chat messages, not chat messages in a chat.
            webUrl (string): Read-only. Link to the message in Microsoft Teams.
            hostedContents (array): Content in a message hosted by Microsoft Teams - for example, images or code snippets.
            replies (array): Replies for a specified message. Supports $expand for channel messages.

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'attachments': attachments,
            'body': body,
            'channelIdentity': channelIdentity,
            'chatId': chatId,
            'createdDateTime': createdDateTime,
            'deletedDateTime': deletedDateTime,
            'etag': etag,
            'eventDetail': eventDetail,
            'from': from_,
            'importance': importance,
            'lastEditedDateTime': lastEditedDateTime,
            'lastModifiedDateTime': lastModifiedDateTime,
            'locale': locale,
            'mentions': mentions,
            'messageHistory': messageHistory,
            'messageType': messageType,
            'policyViolation': policyViolation,
            'reactions': reactions,
            'replyToId': replyToId,
            'subject': subject,
            'summary': summary,
            'webUrl': webUrl,
            'hostedContents': hostedContents,
            'replies': replies,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/messages/{chatMessage_id}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def delete_team_channel_message(self, team_id: str, channel_id: str, chatMessage_id: str) -> Any:
        """
        Delete navigation property messages for teams

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/messages/{chatMessage_id}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def get_replies(self, team_id: str, channel_id: str, chatMessage_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        List replies

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/messages/{chatMessage_id}/replies"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def create_channel_message_reply(self, team_id: str, channel_id: str, chatMessage_id: str, id: Optional[str] = None, attachments: Optional[List[dict[str, dict[str, Any]]]] = None, body: Optional[dict[str, dict[str, Any]]] = None, channelIdentity: Optional[dict[str, dict[str, Any]]] = None, chatId: Optional[str] = None, createdDateTime: Optional[str] = None, deletedDateTime: Optional[str] = None, etag: Optional[str] = None, eventDetail: Optional[dict[str, dict[str, Any]]] = None, from_: Optional[Any] = None, importance: Optional[str] = None, lastEditedDateTime: Optional[str] = None, lastModifiedDateTime: Optional[str] = None, locale: Optional[str] = None, mentions: Optional[List[dict[str, dict[str, Any]]]] = None, messageHistory: Optional[List[dict[str, dict[str, Any]]]] = None, messageType: Optional[str] = None, policyViolation: Optional[dict[str, dict[str, Any]]] = None, reactions: Optional[List[dict[str, dict[str, Any]]]] = None, replyToId: Optional[str] = None, subject: Optional[str] = None, summary: Optional[str] = None, webUrl: Optional[str] = None, hostedContents: Optional[List[Any]] = None, replies: Optional[List[Any]] = None) -> Any:
        """
        Reply to a message in a channel

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id
            id (string): The unique identifier for an entity. Read-only.
            attachments (array): References to attached objects like files, tabs, meetings etc.
            body (object): body
            channelIdentity (object): channelIdentity
            chatId (string): If the message was sent in a chat, represents the identity of the chat.
            createdDateTime (string): Timestamp of when the chat message was created.
            deletedDateTime (string): Read only. Timestamp at which the chat message was deleted, or null if not deleted.
            etag (string): Read-only. Version number of the chat message.
            eventDetail (object): eventDetail
            from_ (string): from
            importance (string): importance
            lastEditedDateTime (string): Read only. Timestamp when edits to the chat message were made. Triggers an 'Edited' flag in the Teams UI. If no edits are made the value is null.
            lastModifiedDateTime (string): Read only. Timestamp when the chat message is created (initial setting) or modified, including when a reaction is added or removed.
            locale (string): Locale of the chat message set by the client. Always set to en-us.
            mentions (array): List of entities mentioned in the chat message. Supported entities are: user, bot, team, channel, chat, and tag.
            messageHistory (array): List of activity history of a message item, including modification time and actions, such as reactionAdded, reactionRemoved, or reaction changes, on the message.
            messageType (string): messageType
            policyViolation (object): policyViolation
            reactions (array): Reactions for this chat message (for example, Like).
            replyToId (string): Read-only. ID of the parent chat message or root chat message of the thread. (Only applies to chat messages in channels, not chats.)
            subject (string): The subject of the chat message, in plaintext.
            summary (string): Summary text of the chat message that could be used for push notifications and summary views or fall back views. Only applies to channel chat messages, not chat messages in a chat.
            webUrl (string): Read-only. Link to the message in Microsoft Teams.
            hostedContents (array): Content in a message hosted by Microsoft Teams - for example, images or code snippets.
            replies (array): Replies for a specified message. Supports $expand for channel messages.

        Returns:
            Any: Created navigation property.

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'attachments': attachments,
            'body': body,
            'channelIdentity': channelIdentity,
            'chatId': chatId,
            'createdDateTime': createdDateTime,
            'deletedDateTime': deletedDateTime,
            'etag': etag,
            'eventDetail': eventDetail,
            'from': from_,
            'importance': importance,
            'lastEditedDateTime': lastEditedDateTime,
            'lastModifiedDateTime': lastModifiedDateTime,
            'locale': locale,
            'mentions': mentions,
            'messageHistory': messageHistory,
            'messageType': messageType,
            'policyViolation': policyViolation,
            'reactions': reactions,
            'replyToId': replyToId,
            'subject': subject,
            'summary': summary,
            'webUrl': webUrl,
            'hostedContents': hostedContents,
            'replies': replies,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/messages/{chatMessage_id}/replies"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def get_chat_message_reply(self, team_id: str, channel_id: str, chatMessage_id: str, chatMessage_id1: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get chatMessage in a channel or chat

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id
            chatMessage_id1 (string): chatMessage-id1
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        if chatMessage_id1 is None:
            raise ValueError("Missing required parameter 'chatMessage-id1'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/messages/{chatMessage_id}/replies/{chatMessage_id1}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_message_reply(self, team_id: str, channel_id: str, chatMessage_id: str, chatMessage_id1: str, id: Optional[str] = None, attachments: Optional[List[dict[str, dict[str, Any]]]] = None, body: Optional[dict[str, dict[str, Any]]] = None, channelIdentity: Optional[dict[str, dict[str, Any]]] = None, chatId: Optional[str] = None, createdDateTime: Optional[str] = None, deletedDateTime: Optional[str] = None, etag: Optional[str] = None, eventDetail: Optional[dict[str, dict[str, Any]]] = None, from_: Optional[Any] = None, importance: Optional[str] = None, lastEditedDateTime: Optional[str] = None, lastModifiedDateTime: Optional[str] = None, locale: Optional[str] = None, mentions: Optional[List[dict[str, dict[str, Any]]]] = None, messageHistory: Optional[List[dict[str, dict[str, Any]]]] = None, messageType: Optional[str] = None, policyViolation: Optional[dict[str, dict[str, Any]]] = None, reactions: Optional[List[dict[str, dict[str, Any]]]] = None, replyToId: Optional[str] = None, subject: Optional[str] = None, summary: Optional[str] = None, webUrl: Optional[str] = None, hostedContents: Optional[List[Any]] = None, replies: Optional[List[Any]] = None) -> Any:
        """
        Update the navigation property replies in teams

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id
            chatMessage_id1 (string): chatMessage-id1
            id (string): The unique identifier for an entity. Read-only.
            attachments (array): References to attached objects like files, tabs, meetings etc.
            body (object): body
            channelIdentity (object): channelIdentity
            chatId (string): If the message was sent in a chat, represents the identity of the chat.
            createdDateTime (string): Timestamp of when the chat message was created.
            deletedDateTime (string): Read only. Timestamp at which the chat message was deleted, or null if not deleted.
            etag (string): Read-only. Version number of the chat message.
            eventDetail (object): eventDetail
            from_ (string): from
            importance (string): importance
            lastEditedDateTime (string): Read only. Timestamp when edits to the chat message were made. Triggers an 'Edited' flag in the Teams UI. If no edits are made the value is null.
            lastModifiedDateTime (string): Read only. Timestamp when the chat message is created (initial setting) or modified, including when a reaction is added or removed.
            locale (string): Locale of the chat message set by the client. Always set to en-us.
            mentions (array): List of entities mentioned in the chat message. Supported entities are: user, bot, team, channel, chat, and tag.
            messageHistory (array): List of activity history of a message item, including modification time and actions, such as reactionAdded, reactionRemoved, or reaction changes, on the message.
            messageType (string): messageType
            policyViolation (object): policyViolation
            reactions (array): Reactions for this chat message (for example, Like).
            replyToId (string): Read-only. ID of the parent chat message or root chat message of the thread. (Only applies to chat messages in channels, not chats.)
            subject (string): The subject of the chat message, in plaintext.
            summary (string): Summary text of the chat message that could be used for push notifications and summary views or fall back views. Only applies to channel chat messages, not chat messages in a chat.
            webUrl (string): Read-only. Link to the message in Microsoft Teams.
            hostedContents (array): Content in a message hosted by Microsoft Teams - for example, images or code snippets.
            replies (array): Replies for a specified message. Supports $expand for channel messages.

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        if chatMessage_id1 is None:
            raise ValueError("Missing required parameter 'chatMessage-id1'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'attachments': attachments,
            'body': body,
            'channelIdentity': channelIdentity,
            'chatId': chatId,
            'createdDateTime': createdDateTime,
            'deletedDateTime': deletedDateTime,
            'etag': etag,
            'eventDetail': eventDetail,
            'from': from_,
            'importance': importance,
            'lastEditedDateTime': lastEditedDateTime,
            'lastModifiedDateTime': lastModifiedDateTime,
            'locale': locale,
            'mentions': mentions,
            'messageHistory': messageHistory,
            'messageType': messageType,
            'policyViolation': policyViolation,
            'reactions': reactions,
            'replyToId': replyToId,
            'subject': subject,
            'summary': summary,
            'webUrl': webUrl,
            'hostedContents': hostedContents,
            'replies': replies,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/messages/{chatMessage_id}/replies/{chatMessage_id1}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def delete_team_channel_message_reply(self, team_id: str, channel_id: str, chatMessage_id: str, chatMessage_id1: str) -> Any:
        """
        Delete navigation property replies for teams

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id
            chatMessage_id1 (string): chatMessage-id1

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        if chatMessage_id1 is None:
            raise ValueError("Missing required parameter 'chatMessage-id1'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/messages/{chatMessage_id}/replies/{chatMessage_id1}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def list_channel_shared_teams(self, team_id: str, channel_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        List sharedWithChannelTeamInfo

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/sharedWithTeams"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def share_channel_with_team(self, team_id: str, channel_id: str, id: Optional[str] = None, displayName: Optional[str] = None, tenantId: Optional[str] = None, team: Optional[Any] = None, isHostTeam: Optional[bool] = None, allowedMembers: Optional[List[Any]] = None) -> Any:
        """
        Create new navigation property to sharedWithTeams for teams

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            id (string): The unique identifier for an entity. Read-only.
            displayName (string): The name of the team.
            tenantId (string): The ID of the Microsoft Entra tenant.
            team (string): team
            isHostTeam (boolean): Indicates whether the team is the host of the channel.
            allowedMembers (array): A collection of team members who have access to the shared channel.

        Returns:
            Any: Created navigation property.

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'displayName': displayName,
            'tenantId': tenantId,
            'team': team,
            'isHostTeam': isHostTeam,
            'allowedMembers': allowedMembers,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/sharedWithTeams"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def get_shared_teams_channels_info(self, team_id: str, channel_id: str, sharedWithChannelTeamInfo_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get sharedWithChannelTeamInfo

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            sharedWithChannelTeamInfo_id (string): sharedWithChannelTeamInfo-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if sharedWithChannelTeamInfo_id is None:
            raise ValueError("Missing required parameter 'sharedWithChannelTeamInfo-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/sharedWithTeams/{sharedWithChannelTeamInfo_id}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_shared_with_team_info(self, team_id: str, channel_id: str, sharedWithChannelTeamInfo_id: str, id: Optional[str] = None, displayName: Optional[str] = None, tenantId: Optional[str] = None, team: Optional[Any] = None, isHostTeam: Optional[bool] = None, allowedMembers: Optional[List[Any]] = None) -> Any:
        """
        Update the navigation property sharedWithTeams in teams

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            sharedWithChannelTeamInfo_id (string): sharedWithChannelTeamInfo-id
            id (string): The unique identifier for an entity. Read-only.
            displayName (string): The name of the team.
            tenantId (string): The ID of the Microsoft Entra tenant.
            team (string): team
            isHostTeam (boolean): Indicates whether the team is the host of the channel.
            allowedMembers (array): A collection of team members who have access to the shared channel.

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if sharedWithChannelTeamInfo_id is None:
            raise ValueError("Missing required parameter 'sharedWithChannelTeamInfo-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'displayName': displayName,
            'tenantId': tenantId,
            'team': team,
            'isHostTeam': isHostTeam,
            'allowedMembers': allowedMembers,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/sharedWithTeams/{sharedWithChannelTeamInfo_id}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def delete_shared_team_channel_link(self, team_id: str, channel_id: str, sharedWithChannelTeamInfo_id: str) -> Any:
        """
        Delete sharedWithChannelTeamInfo

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            sharedWithChannelTeamInfo_id (string): sharedWithChannelTeamInfo-id

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if sharedWithChannelTeamInfo_id is None:
            raise ValueError("Missing required parameter 'sharedWithChannelTeamInfo-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/sharedWithTeams/{sharedWithChannelTeamInfo_id}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def list_channel_allowed_members(self, team_id: str, channel_id: str, sharedWithChannelTeamInfo_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        List allowedMembers

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            sharedWithChannelTeamInfo_id (string): sharedWithChannelTeamInfo-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if sharedWithChannelTeamInfo_id is None:
            raise ValueError("Missing required parameter 'sharedWithChannelTeamInfo-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/sharedWithTeams/{sharedWithChannelTeamInfo_id}/allowedMembers"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def get_channel_allowed_member_by_id(self, team_id: str, channel_id: str, sharedWithChannelTeamInfo_id: str, conversationMember_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get allowedMembers from teams

        Args:
            team_id (string): team-id
            channel_id (string): channel-id
            sharedWithChannelTeamInfo_id (string): sharedWithChannelTeamInfo-id
            conversationMember_id (string): conversationMember-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            teams.channel
        """
        if team_id is None:
            raise ValueError("Missing required parameter 'team-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if sharedWithChannelTeamInfo_id is None:
            raise ValueError("Missing required parameter 'sharedWithChannelTeamInfo-id'.")
        if conversationMember_id is None:
            raise ValueError("Missing required parameter 'conversationMember-id'.")
        url = f"{self.base_url}/teams/{team_id}/channels/{channel_id}/sharedWithTeams/{sharedWithChannelTeamInfo_id}/allowedMembers/{conversationMember_id}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def list_chats(self, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        List chats

        Args:
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chat
        """
        url = f"{self.base_url}/chats"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def create_chat_operation(self, id: Optional[str] = None, chatType: Optional[str] = None, createdDateTime: Optional[str] = None, isHiddenForAllMembers: Optional[bool] = None, lastUpdatedDateTime: Optional[str] = None, onlineMeetingInfo: Optional[dict[str, dict[str, Any]]] = None, tenantId: Optional[str] = None, topic: Optional[str] = None, viewpoint: Optional[dict[str, dict[str, Any]]] = None, webUrl: Optional[str] = None, installedApps: Optional[List[Any]] = None, lastMessagePreview: Optional[Any] = None, members: Optional[List[Any]] = None, messages: Optional[List[Any]] = None, permissionGrants: Optional[List[Any]] = None, pinnedMessages: Optional[List[Any]] = None, tabs: Optional[List[Any]] = None) -> Any:
        """
        Create chat

        Args:
            id (string): The unique identifier for an entity. Read-only.
            chatType (string): chatType
            createdDateTime (string): Date and time at which the chat was created. Read-only.
            isHiddenForAllMembers (boolean): Indicates whether the chat is hidden for all its members. Read-only.
            lastUpdatedDateTime (string): Date and time at which the chat was renamed or the list of members was last changed. Read-only.
            onlineMeetingInfo (object): onlineMeetingInfo
            tenantId (string): The identifier of the tenant in which the chat was created. Read-only.
            topic (string): (Optional) Subject or topic for the chat. Only available for group chats.
            viewpoint (object): viewpoint
            webUrl (string): The URL for the chat in Microsoft Teams. The URL should be treated as an opaque blob, and not parsed. Read-only.
            installedApps (array): A collection of all the apps in the chat. Nullable.
            lastMessagePreview (string): lastMessagePreview
            members (array): A collection of all the members in the chat. Nullable.
            messages (array): A collection of all the messages in the chat. Nullable.
            permissionGrants (array): A collection of permissions granted to apps for the chat.
            pinnedMessages (array): A collection of all the pinned messages in the chat. Nullable.
            tabs (array): A collection of all the tabs in the chat. Nullable.

        Returns:
            Any: Created entity

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chat
        """
        request_body_data = None
        request_body_data = {
            'id': id,
            'chatType': chatType,
            'createdDateTime': createdDateTime,
            'isHiddenForAllMembers': isHiddenForAllMembers,
            'lastUpdatedDateTime': lastUpdatedDateTime,
            'onlineMeetingInfo': onlineMeetingInfo,
            'tenantId': tenantId,
            'topic': topic,
            'viewpoint': viewpoint,
            'webUrl': webUrl,
            'installedApps': installedApps,
            'lastMessagePreview': lastMessagePreview,
            'members': members,
            'messages': messages,
            'permissionGrants': permissionGrants,
            'pinnedMessages': pinnedMessages,
            'tabs': tabs,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/chats"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def get_chat(self, chat_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get chat

        Args:
            chat_id (string): chat-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved entity

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chat
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        url = f"{self.base_url}/chats/{chat_id}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_chat_details(self, chat_id: str, id: Optional[str] = None, chatType: Optional[str] = None, createdDateTime: Optional[str] = None, isHiddenForAllMembers: Optional[bool] = None, lastUpdatedDateTime: Optional[str] = None, onlineMeetingInfo: Optional[dict[str, dict[str, Any]]] = None, tenantId: Optional[str] = None, topic: Optional[str] = None, viewpoint: Optional[dict[str, dict[str, Any]]] = None, webUrl: Optional[str] = None, installedApps: Optional[List[Any]] = None, lastMessagePreview: Optional[Any] = None, members: Optional[List[Any]] = None, messages: Optional[List[Any]] = None, permissionGrants: Optional[List[Any]] = None, pinnedMessages: Optional[List[Any]] = None, tabs: Optional[List[Any]] = None) -> Any:
        """
        Update chat

        Args:
            chat_id (string): chat-id
            id (string): The unique identifier for an entity. Read-only.
            chatType (string): chatType
            createdDateTime (string): Date and time at which the chat was created. Read-only.
            isHiddenForAllMembers (boolean): Indicates whether the chat is hidden for all its members. Read-only.
            lastUpdatedDateTime (string): Date and time at which the chat was renamed or the list of members was last changed. Read-only.
            onlineMeetingInfo (object): onlineMeetingInfo
            tenantId (string): The identifier of the tenant in which the chat was created. Read-only.
            topic (string): (Optional) Subject or topic for the chat. Only available for group chats.
            viewpoint (object): viewpoint
            webUrl (string): The URL for the chat in Microsoft Teams. The URL should be treated as an opaque blob, and not parsed. Read-only.
            installedApps (array): A collection of all the apps in the chat. Nullable.
            lastMessagePreview (string): lastMessagePreview
            members (array): A collection of all the members in the chat. Nullable.
            messages (array): A collection of all the messages in the chat. Nullable.
            permissionGrants (array): A collection of permissions granted to apps for the chat.
            pinnedMessages (array): A collection of all the pinned messages in the chat. Nullable.
            tabs (array): A collection of all the tabs in the chat. Nullable.

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chat
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'chatType': chatType,
            'createdDateTime': createdDateTime,
            'isHiddenForAllMembers': isHiddenForAllMembers,
            'lastUpdatedDateTime': lastUpdatedDateTime,
            'onlineMeetingInfo': onlineMeetingInfo,
            'tenantId': tenantId,
            'topic': topic,
            'viewpoint': viewpoint,
            'webUrl': webUrl,
            'installedApps': installedApps,
            'lastMessagePreview': lastMessagePreview,
            'members': members,
            'messages': messages,
            'permissionGrants': permissionGrants,
            'pinnedMessages': pinnedMessages,
            'tabs': tabs,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/chats/{chat_id}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def delete_chat_by_id(self, chat_id: str) -> Any:
        """
        Delete chat

        Args:
            chat_id (string): chat-id

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chat
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        url = f"{self.base_url}/chats/{chat_id}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def list_chat_members(self, chat_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        List conversationMembers

        Args:
            chat_id (string): chat-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.conversationMember
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        url = f"{self.base_url}/chats/{chat_id}/members"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def add_member_to_chat(self, chat_id: str, id: Optional[str] = None, displayName: Optional[str] = None, roles: Optional[List[str]] = None, visibleHistoryStartDateTime: Optional[str] = None) -> Any:
        """
        Add member to a chat

        Args:
            chat_id (string): chat-id
            id (string): The unique identifier for an entity. Read-only.
            displayName (string): The display name of the user.
            roles (array): The roles for that user. This property contains more qualifiers only when relevant - for example, if the member has owner privileges, the roles property contains owner as one of the values. Similarly, if the member is an in-tenant guest, the roles property contains guest as one of the values. A basic member shouldn't have any values specified in the roles property. An Out-of-tenant external member is assigned the owner role.
            visibleHistoryStartDateTime (string): The timestamp denoting how far back a conversation's history is shared with the conversation member. This property is settable only for members of a chat.

        Returns:
            Any: Created navigation property.

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.conversationMember
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'displayName': displayName,
            'roles': roles,
            'visibleHistoryStartDateTime': visibleHistoryStartDateTime,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/chats/{chat_id}/members"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def get_conversation_member(self, chat_id: str, conversationMember_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get conversationMember

        Args:
            chat_id (string): chat-id
            conversationMember_id (string): conversationMember-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.conversationMember
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        if conversationMember_id is None:
            raise ValueError("Missing required parameter 'conversationMember-id'.")
        url = f"{self.base_url}/chats/{chat_id}/members/{conversationMember_id}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_chat_member(self, chat_id: str, conversationMember_id: str, id: Optional[str] = None, displayName: Optional[str] = None, roles: Optional[List[str]] = None, visibleHistoryStartDateTime: Optional[str] = None) -> Any:
        """
        Update the navigation property members in chats

        Args:
            chat_id (string): chat-id
            conversationMember_id (string): conversationMember-id
            id (string): The unique identifier for an entity. Read-only.
            displayName (string): The display name of the user.
            roles (array): The roles for that user. This property contains more qualifiers only when relevant - for example, if the member has owner privileges, the roles property contains owner as one of the values. Similarly, if the member is an in-tenant guest, the roles property contains guest as one of the values. A basic member shouldn't have any values specified in the roles property. An Out-of-tenant external member is assigned the owner role.
            visibleHistoryStartDateTime (string): The timestamp denoting how far back a conversation's history is shared with the conversation member. This property is settable only for members of a chat.

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.conversationMember
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        if conversationMember_id is None:
            raise ValueError("Missing required parameter 'conversationMember-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'displayName': displayName,
            'roles': roles,
            'visibleHistoryStartDateTime': visibleHistoryStartDateTime,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/chats/{chat_id}/members/{conversationMember_id}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def remove_conversation_member(self, chat_id: str, conversationMember_id: str) -> Any:
        """
        Remove member from chat

        Args:
            chat_id (string): chat-id
            conversationMember_id (string): conversationMember-id

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.conversationMember
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        if conversationMember_id is None:
            raise ValueError("Missing required parameter 'conversationMember-id'.")
        url = f"{self.base_url}/chats/{chat_id}/members/{conversationMember_id}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def list_chat_messages(self, chat_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        List messages in a chat

        Args:
            chat_id (string): chat-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chatMessage
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        url = f"{self.base_url}/chats/{chat_id}/messages"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def post_chat_message(self, chat_id: str, id: Optional[str] = None, attachments: Optional[List[dict[str, dict[str, Any]]]] = None, body: Optional[dict[str, dict[str, Any]]] = None, channelIdentity: Optional[dict[str, dict[str, Any]]] = None, chatId: Optional[str] = None, createdDateTime: Optional[str] = None, deletedDateTime: Optional[str] = None, etag: Optional[str] = None, eventDetail: Optional[dict[str, dict[str, Any]]] = None, from_: Optional[Any] = None, importance: Optional[str] = None, lastEditedDateTime: Optional[str] = None, lastModifiedDateTime: Optional[str] = None, locale: Optional[str] = None, mentions: Optional[List[dict[str, dict[str, Any]]]] = None, messageHistory: Optional[List[dict[str, dict[str, Any]]]] = None, messageType: Optional[str] = None, policyViolation: Optional[dict[str, dict[str, Any]]] = None, reactions: Optional[List[dict[str, dict[str, Any]]]] = None, replyToId: Optional[str] = None, subject: Optional[str] = None, summary: Optional[str] = None, webUrl: Optional[str] = None, hostedContents: Optional[List[Any]] = None, replies: Optional[List[Any]] = None) -> Any:
        """
        Send chatMessage in a channel or a chat

        Args:
            chat_id (string): chat-id
            id (string): The unique identifier for an entity. Read-only.
            attachments (array): References to attached objects like files, tabs, meetings etc.
            body (object): body
            channelIdentity (object): channelIdentity
            chatId (string): If the message was sent in a chat, represents the identity of the chat.
            createdDateTime (string): Timestamp of when the chat message was created.
            deletedDateTime (string): Read only. Timestamp at which the chat message was deleted, or null if not deleted.
            etag (string): Read-only. Version number of the chat message.
            eventDetail (object): eventDetail
            from_ (string): from
            importance (string): importance
            lastEditedDateTime (string): Read only. Timestamp when edits to the chat message were made. Triggers an 'Edited' flag in the Teams UI. If no edits are made the value is null.
            lastModifiedDateTime (string): Read only. Timestamp when the chat message is created (initial setting) or modified, including when a reaction is added or removed.
            locale (string): Locale of the chat message set by the client. Always set to en-us.
            mentions (array): List of entities mentioned in the chat message. Supported entities are: user, bot, team, channel, chat, and tag.
            messageHistory (array): List of activity history of a message item, including modification time and actions, such as reactionAdded, reactionRemoved, or reaction changes, on the message.
            messageType (string): messageType
            policyViolation (object): policyViolation
            reactions (array): Reactions for this chat message (for example, Like).
            replyToId (string): Read-only. ID of the parent chat message or root chat message of the thread. (Only applies to chat messages in channels, not chats.)
            subject (string): The subject of the chat message, in plaintext.
            summary (string): Summary text of the chat message that could be used for push notifications and summary views or fall back views. Only applies to channel chat messages, not chat messages in a chat.
            webUrl (string): Read-only. Link to the message in Microsoft Teams.
            hostedContents (array): Content in a message hosted by Microsoft Teams - for example, images or code snippets.
            replies (array): Replies for a specified message. Supports $expand for channel messages.

        Returns:
            Any: Created navigation property.

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chatMessage
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'attachments': attachments,
            'body': body,
            'channelIdentity': channelIdentity,
            'chatId': chatId,
            'createdDateTime': createdDateTime,
            'deletedDateTime': deletedDateTime,
            'etag': etag,
            'eventDetail': eventDetail,
            'from': from_,
            'importance': importance,
            'lastEditedDateTime': lastEditedDateTime,
            'lastModifiedDateTime': lastModifiedDateTime,
            'locale': locale,
            'mentions': mentions,
            'messageHistory': messageHistory,
            'messageType': messageType,
            'policyViolation': policyViolation,
            'reactions': reactions,
            'replyToId': replyToId,
            'subject': subject,
            'summary': summary,
            'webUrl': webUrl,
            'hostedContents': hostedContents,
            'replies': replies,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/chats/{chat_id}/messages"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def get_chat_message_detail(self, chat_id: str, chatMessage_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get chatMessage in a channel or chat

        Args:
            chat_id (string): chat-id
            chatMessage_id (string): chatMessage-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chatMessage
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        url = f"{self.base_url}/chats/{chat_id}/messages/{chatMessage_id}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_chat_messages(self, chat_id: str, chatMessage_id: str, id: Optional[str] = None, attachments: Optional[List[dict[str, dict[str, Any]]]] = None, body: Optional[dict[str, dict[str, Any]]] = None, channelIdentity: Optional[dict[str, dict[str, Any]]] = None, chatId: Optional[str] = None, createdDateTime: Optional[str] = None, deletedDateTime: Optional[str] = None, etag: Optional[str] = None, eventDetail: Optional[dict[str, dict[str, Any]]] = None, from_: Optional[Any] = None, importance: Optional[str] = None, lastEditedDateTime: Optional[str] = None, lastModifiedDateTime: Optional[str] = None, locale: Optional[str] = None, mentions: Optional[List[dict[str, dict[str, Any]]]] = None, messageHistory: Optional[List[dict[str, dict[str, Any]]]] = None, messageType: Optional[str] = None, policyViolation: Optional[dict[str, dict[str, Any]]] = None, reactions: Optional[List[dict[str, dict[str, Any]]]] = None, replyToId: Optional[str] = None, subject: Optional[str] = None, summary: Optional[str] = None, webUrl: Optional[str] = None, hostedContents: Optional[List[Any]] = None, replies: Optional[List[Any]] = None) -> Any:
        """
        Update the navigation property messages in chats

        Args:
            chat_id (string): chat-id
            chatMessage_id (string): chatMessage-id
            id (string): The unique identifier for an entity. Read-only.
            attachments (array): References to attached objects like files, tabs, meetings etc.
            body (object): body
            channelIdentity (object): channelIdentity
            chatId (string): If the message was sent in a chat, represents the identity of the chat.
            createdDateTime (string): Timestamp of when the chat message was created.
            deletedDateTime (string): Read only. Timestamp at which the chat message was deleted, or null if not deleted.
            etag (string): Read-only. Version number of the chat message.
            eventDetail (object): eventDetail
            from_ (string): from
            importance (string): importance
            lastEditedDateTime (string): Read only. Timestamp when edits to the chat message were made. Triggers an 'Edited' flag in the Teams UI. If no edits are made the value is null.
            lastModifiedDateTime (string): Read only. Timestamp when the chat message is created (initial setting) or modified, including when a reaction is added or removed.
            locale (string): Locale of the chat message set by the client. Always set to en-us.
            mentions (array): List of entities mentioned in the chat message. Supported entities are: user, bot, team, channel, chat, and tag.
            messageHistory (array): List of activity history of a message item, including modification time and actions, such as reactionAdded, reactionRemoved, or reaction changes, on the message.
            messageType (string): messageType
            policyViolation (object): policyViolation
            reactions (array): Reactions for this chat message (for example, Like).
            replyToId (string): Read-only. ID of the parent chat message or root chat message of the thread. (Only applies to chat messages in channels, not chats.)
            subject (string): The subject of the chat message, in plaintext.
            summary (string): Summary text of the chat message that could be used for push notifications and summary views or fall back views. Only applies to channel chat messages, not chat messages in a chat.
            webUrl (string): Read-only. Link to the message in Microsoft Teams.
            hostedContents (array): Content in a message hosted by Microsoft Teams - for example, images or code snippets.
            replies (array): Replies for a specified message. Supports $expand for channel messages.

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chatMessage
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'attachments': attachments,
            'body': body,
            'channelIdentity': channelIdentity,
            'chatId': chatId,
            'createdDateTime': createdDateTime,
            'deletedDateTime': deletedDateTime,
            'etag': etag,
            'eventDetail': eventDetail,
            'from': from_,
            'importance': importance,
            'lastEditedDateTime': lastEditedDateTime,
            'lastModifiedDateTime': lastModifiedDateTime,
            'locale': locale,
            'mentions': mentions,
            'messageHistory': messageHistory,
            'messageType': messageType,
            'policyViolation': policyViolation,
            'reactions': reactions,
            'replyToId': replyToId,
            'subject': subject,
            'summary': summary,
            'webUrl': webUrl,
            'hostedContents': hostedContents,
            'replies': replies,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/chats/{chat_id}/messages/{chatMessage_id}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def delete_chat_messages(self, chat_id: str, chatMessage_id: str) -> Any:
        """
        Delete navigation property messages for chats

        Args:
            chat_id (string): chat-id
            chatMessage_id (string): chatMessage-id

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chatMessage
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        url = f"{self.base_url}/chats/{chat_id}/messages/{chatMessage_id}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def read_chat_replies(self, chat_id: str, chatMessage_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        Get replies from chats

        Args:
            chat_id (string): chat-id
            chatMessage_id (string): chatMessage-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chatMessage
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        url = f"{self.base_url}/chats/{chat_id}/messages/{chatMessage_id}/replies"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def create_chat_reply(self, chat_id: str, chatMessage_id: str, id: Optional[str] = None, attachments: Optional[List[dict[str, dict[str, Any]]]] = None, body: Optional[dict[str, dict[str, Any]]] = None, channelIdentity: Optional[dict[str, dict[str, Any]]] = None, chatId: Optional[str] = None, createdDateTime: Optional[str] = None, deletedDateTime: Optional[str] = None, etag: Optional[str] = None, eventDetail: Optional[dict[str, dict[str, Any]]] = None, from_: Optional[Any] = None, importance: Optional[str] = None, lastEditedDateTime: Optional[str] = None, lastModifiedDateTime: Optional[str] = None, locale: Optional[str] = None, mentions: Optional[List[dict[str, dict[str, Any]]]] = None, messageHistory: Optional[List[dict[str, dict[str, Any]]]] = None, messageType: Optional[str] = None, policyViolation: Optional[dict[str, dict[str, Any]]] = None, reactions: Optional[List[dict[str, dict[str, Any]]]] = None, replyToId: Optional[str] = None, subject: Optional[str] = None, summary: Optional[str] = None, webUrl: Optional[str] = None, hostedContents: Optional[List[Any]] = None, replies: Optional[List[Any]] = None) -> Any:
        """
        Create new navigation property to replies for chats

        Args:
            chat_id (string): chat-id
            chatMessage_id (string): chatMessage-id
            id (string): The unique identifier for an entity. Read-only.
            attachments (array): References to attached objects like files, tabs, meetings etc.
            body (object): body
            channelIdentity (object): channelIdentity
            chatId (string): If the message was sent in a chat, represents the identity of the chat.
            createdDateTime (string): Timestamp of when the chat message was created.
            deletedDateTime (string): Read only. Timestamp at which the chat message was deleted, or null if not deleted.
            etag (string): Read-only. Version number of the chat message.
            eventDetail (object): eventDetail
            from_ (string): from
            importance (string): importance
            lastEditedDateTime (string): Read only. Timestamp when edits to the chat message were made. Triggers an 'Edited' flag in the Teams UI. If no edits are made the value is null.
            lastModifiedDateTime (string): Read only. Timestamp when the chat message is created (initial setting) or modified, including when a reaction is added or removed.
            locale (string): Locale of the chat message set by the client. Always set to en-us.
            mentions (array): List of entities mentioned in the chat message. Supported entities are: user, bot, team, channel, chat, and tag.
            messageHistory (array): List of activity history of a message item, including modification time and actions, such as reactionAdded, reactionRemoved, or reaction changes, on the message.
            messageType (string): messageType
            policyViolation (object): policyViolation
            reactions (array): Reactions for this chat message (for example, Like).
            replyToId (string): Read-only. ID of the parent chat message or root chat message of the thread. (Only applies to chat messages in channels, not chats.)
            subject (string): The subject of the chat message, in plaintext.
            summary (string): Summary text of the chat message that could be used for push notifications and summary views or fall back views. Only applies to channel chat messages, not chat messages in a chat.
            webUrl (string): Read-only. Link to the message in Microsoft Teams.
            hostedContents (array): Content in a message hosted by Microsoft Teams - for example, images or code snippets.
            replies (array): Replies for a specified message. Supports $expand for channel messages.

        Returns:
            Any: Created navigation property.

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chatMessage
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'attachments': attachments,
            'body': body,
            'channelIdentity': channelIdentity,
            'chatId': chatId,
            'createdDateTime': createdDateTime,
            'deletedDateTime': deletedDateTime,
            'etag': etag,
            'eventDetail': eventDetail,
            'from': from_,
            'importance': importance,
            'lastEditedDateTime': lastEditedDateTime,
            'lastModifiedDateTime': lastModifiedDateTime,
            'locale': locale,
            'mentions': mentions,
            'messageHistory': messageHistory,
            'messageType': messageType,
            'policyViolation': policyViolation,
            'reactions': reactions,
            'replyToId': replyToId,
            'subject': subject,
            'summary': summary,
            'webUrl': webUrl,
            'hostedContents': hostedContents,
            'replies': replies,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/chats/{chat_id}/messages/{chatMessage_id}/replies"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def get_chat_replies(self, chat_id: str, chatMessage_id: str, chatMessage_id1: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get replies from chats

        Args:
            chat_id (string): chat-id
            chatMessage_id (string): chatMessage-id
            chatMessage_id1 (string): chatMessage-id1
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chatMessage
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        if chatMessage_id1 is None:
            raise ValueError("Missing required parameter 'chatMessage-id1'.")
        url = f"{self.base_url}/chats/{chat_id}/messages/{chatMessage_id}/replies/{chatMessage_id1}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_chat_replies(self, chat_id: str, chatMessage_id: str, chatMessage_id1: str, id: Optional[str] = None, attachments: Optional[List[dict[str, dict[str, Any]]]] = None, body: Optional[dict[str, dict[str, Any]]] = None, channelIdentity: Optional[dict[str, dict[str, Any]]] = None, chatId: Optional[str] = None, createdDateTime: Optional[str] = None, deletedDateTime: Optional[str] = None, etag: Optional[str] = None, eventDetail: Optional[dict[str, dict[str, Any]]] = None, from_: Optional[Any] = None, importance: Optional[str] = None, lastEditedDateTime: Optional[str] = None, lastModifiedDateTime: Optional[str] = None, locale: Optional[str] = None, mentions: Optional[List[dict[str, dict[str, Any]]]] = None, messageHistory: Optional[List[dict[str, dict[str, Any]]]] = None, messageType: Optional[str] = None, policyViolation: Optional[dict[str, dict[str, Any]]] = None, reactions: Optional[List[dict[str, dict[str, Any]]]] = None, replyToId: Optional[str] = None, subject: Optional[str] = None, summary: Optional[str] = None, webUrl: Optional[str] = None, hostedContents: Optional[List[Any]] = None, replies: Optional[List[Any]] = None) -> Any:
        """
        Update the navigation property replies in chats

        Args:
            chat_id (string): chat-id
            chatMessage_id (string): chatMessage-id
            chatMessage_id1 (string): chatMessage-id1
            id (string): The unique identifier for an entity. Read-only.
            attachments (array): References to attached objects like files, tabs, meetings etc.
            body (object): body
            channelIdentity (object): channelIdentity
            chatId (string): If the message was sent in a chat, represents the identity of the chat.
            createdDateTime (string): Timestamp of when the chat message was created.
            deletedDateTime (string): Read only. Timestamp at which the chat message was deleted, or null if not deleted.
            etag (string): Read-only. Version number of the chat message.
            eventDetail (object): eventDetail
            from_ (string): from
            importance (string): importance
            lastEditedDateTime (string): Read only. Timestamp when edits to the chat message were made. Triggers an 'Edited' flag in the Teams UI. If no edits are made the value is null.
            lastModifiedDateTime (string): Read only. Timestamp when the chat message is created (initial setting) or modified, including when a reaction is added or removed.
            locale (string): Locale of the chat message set by the client. Always set to en-us.
            mentions (array): List of entities mentioned in the chat message. Supported entities are: user, bot, team, channel, chat, and tag.
            messageHistory (array): List of activity history of a message item, including modification time and actions, such as reactionAdded, reactionRemoved, or reaction changes, on the message.
            messageType (string): messageType
            policyViolation (object): policyViolation
            reactions (array): Reactions for this chat message (for example, Like).
            replyToId (string): Read-only. ID of the parent chat message or root chat message of the thread. (Only applies to chat messages in channels, not chats.)
            subject (string): The subject of the chat message, in plaintext.
            summary (string): Summary text of the chat message that could be used for push notifications and summary views or fall back views. Only applies to channel chat messages, not chat messages in a chat.
            webUrl (string): Read-only. Link to the message in Microsoft Teams.
            hostedContents (array): Content in a message hosted by Microsoft Teams - for example, images or code snippets.
            replies (array): Replies for a specified message. Supports $expand for channel messages.

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chatMessage
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        if chatMessage_id1 is None:
            raise ValueError("Missing required parameter 'chatMessage-id1'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'attachments': attachments,
            'body': body,
            'channelIdentity': channelIdentity,
            'chatId': chatId,
            'createdDateTime': createdDateTime,
            'deletedDateTime': deletedDateTime,
            'etag': etag,
            'eventDetail': eventDetail,
            'from': from_,
            'importance': importance,
            'lastEditedDateTime': lastEditedDateTime,
            'lastModifiedDateTime': lastModifiedDateTime,
            'locale': locale,
            'mentions': mentions,
            'messageHistory': messageHistory,
            'messageType': messageType,
            'policyViolation': policyViolation,
            'reactions': reactions,
            'replyToId': replyToId,
            'subject': subject,
            'summary': summary,
            'webUrl': webUrl,
            'hostedContents': hostedContents,
            'replies': replies,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/chats/{chat_id}/messages/{chatMessage_id}/replies/{chatMessage_id1}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def delete_chat_reply(self, chat_id: str, chatMessage_id: str, chatMessage_id1: str) -> Any:
        """
        Delete navigation property replies for chats

        Args:
            chat_id (string): chat-id
            chatMessage_id (string): chatMessage-id
            chatMessage_id1 (string): chatMessage-id1

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            chats.chatMessage
        """
        if chat_id is None:
            raise ValueError("Missing required parameter 'chat-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        if chatMessage_id1 is None:
            raise ValueError("Missing required parameter 'chatMessage-id1'.")
        url = f"{self.base_url}/chats/{chat_id}/messages/{chatMessage_id}/replies/{chatMessage_id1}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def get_group_team(self, group_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get team from groups

        Args:
            group_id (string): group-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        url = f"{self.base_url}/groups/{group_id}/team"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def create_team_from_group(self, group_id: str, id: Optional[str] = None, classification: Optional[str] = None, createdDateTime: Optional[str] = None, description: Optional[str] = None, displayName: Optional[str] = None, firstChannelName: Optional[str] = None, funSettings: Optional[dict[str, dict[str, Any]]] = None, guestSettings: Optional[dict[str, dict[str, Any]]] = None, internalId: Optional[str] = None, isArchived: Optional[bool] = None, memberSettings: Optional[dict[str, dict[str, Any]]] = None, messagingSettings: Optional[dict[str, dict[str, Any]]] = None, specialization: Optional[str] = None, summary: Optional[dict[str, dict[str, Any]]] = None, tenantId: Optional[str] = None, visibility: Optional[str] = None, webUrl: Optional[str] = None, allChannels: Optional[List[Any]] = None, channels: Optional[List[Any]] = None, group: Optional[Any] = None, incomingChannels: Optional[List[Any]] = None, installedApps: Optional[List[Any]] = None, members: Optional[List[Any]] = None, operations: Optional[List[Any]] = None, permissionGrants: Optional[List[Any]] = None, photo: Optional[Any] = None, primaryChannel: Optional[Any] = None, schedule: Optional[Any] = None, tags: Optional[List[Any]] = None, template: Optional[Any] = None) -> Any:
        """
        Create team from group

        Args:
            group_id (string): group-id
            id (string): The unique identifier for an entity. Read-only.
            classification (string): An optional label. Typically describes the data or business sensitivity of the team. Must match one of a preconfigured set in the tenant's directory.
            createdDateTime (string): Timestamp at which the team was created.
            description (string): An optional description for the team. Maximum length: 1,024 characters.
            displayName (string): The name of the team.
            firstChannelName (string): The name of the first channel in the team. This is an optional property, only used during team creation and isn't returned in methods to get and list teams.
            funSettings (object): funSettings
            guestSettings (object): guestSettings
            internalId (string): A unique ID for the team that was used in a few places such as the audit log/Office 365 Management Activity API.
            isArchived (boolean): Whether this team is in read-only mode.
            memberSettings (object): memberSettings
            messagingSettings (object): messagingSettings
            specialization (string): specialization
            summary (object): summary
            tenantId (string): The ID of the Microsoft Entra tenant.
            visibility (string): visibility
            webUrl (string): A hyperlink that goes to the team in the Microsoft Teams client. You get this URL when you right-click a team in the Microsoft Teams client and select Get link to team. This URL should be treated as an opaque blob, and not parsed.
            allChannels (array): List of channels either hosted in or shared with the team (incoming channels).
            channels (array): The collection of channels and messages associated with the team.
            group (string): group
            incomingChannels (array): List of channels shared with the team.
            installedApps (array): The apps installed in this team.
            members (array): Members and owners of the team.
            operations (array): The async operations that ran or are running on this team.
            permissionGrants (array): A collection of permissions granted to apps to access the team.
            photo (string): photo
            primaryChannel (string): primaryChannel
            schedule (string): schedule
            tags (array): The tags associated with the team.
            template (string): template

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'classification': classification,
            'createdDateTime': createdDateTime,
            'description': description,
            'displayName': displayName,
            'firstChannelName': firstChannelName,
            'funSettings': funSettings,
            'guestSettings': guestSettings,
            'internalId': internalId,
            'isArchived': isArchived,
            'memberSettings': memberSettings,
            'messagingSettings': messagingSettings,
            'specialization': specialization,
            'summary': summary,
            'tenantId': tenantId,
            'visibility': visibility,
            'webUrl': webUrl,
            'allChannels': allChannels,
            'channels': channels,
            'group': group,
            'incomingChannels': incomingChannels,
            'installedApps': installedApps,
            'members': members,
            'operations': operations,
            'permissionGrants': permissionGrants,
            'photo': photo,
            'primaryChannel': primaryChannel,
            'schedule': schedule,
            'tags': tags,
            'template': template,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/groups/{group_id}/team"
        query_params = {}
        return self._put_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def delete_group_team(self, group_id: str) -> Any:
        """
        Delete navigation property team for groups

        Args:
            group_id (string): group-id

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        url = f"{self.base_url}/groups/{group_id}/team"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def fetch_groups_team_all_channels(self, group_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        Get allChannels from groups

        Args:
            group_id (string): group-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        url = f"{self.base_url}/groups/{group_id}/team/allChannels"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def get_group_team_all_channels(self, group_id: str, channel_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get allChannels from groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        url = f"{self.base_url}/groups/{group_id}/team/allChannels/{channel_id}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def get_group_channels(self, group_id: str, channel_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get channels from groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_group_channels(self, group_id: str, channel_id: str, id: Optional[str] = None, createdDateTime: Optional[str] = None, description: Optional[str] = None, displayName: Optional[str] = None, email: Optional[str] = None, isArchived: Optional[bool] = None, isFavoriteByDefault: Optional[bool] = None, membershipType: Optional[str] = None, summary: Optional[dict[str, dict[str, Any]]] = None, tenantId: Optional[str] = None, webUrl: Optional[str] = None, allMembers: Optional[List[Any]] = None, filesFolder: Optional[Any] = None, members: Optional[List[Any]] = None, messages: Optional[List[Any]] = None, sharedWithTeams: Optional[List[Any]] = None, tabs: Optional[List[Any]] = None) -> Any:
        """
        Update the navigation property channels in groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            id (string): The unique identifier for an entity. Read-only.
            createdDateTime (string): Read only. Timestamp at which the channel was created.
            description (string): Optional textual description for the channel.
            displayName (string): Channel name as it will appear to the user in Microsoft Teams. The maximum length is 50 characters.
            email (string): The email address for sending messages to the channel. Read-only.
            isArchived (boolean): Indicates whether the channel is archived. Read-only.
            isFavoriteByDefault (boolean): Indicates whether the channel should be marked as recommended for all members of the team to show in their channel list. Note: All recommended channels automatically show in the channels list for education and frontline worker users. The property can only be set programmatically via the Create team method. The default value is false.
            membershipType (string): membershipType
            summary (object): summary
            tenantId (string): The ID of the Microsoft Entra tenant.
            webUrl (string): A hyperlink that will go to the channel in Microsoft Teams. This is the URL that you get when you right-click a channel in Microsoft Teams and select Get link to channel. This URL should be treated as an opaque blob, and not parsed. Read-only.
            allMembers (array): A collection of membership records associated with the channel, including both direct and indirect members of shared channels.
            filesFolder (string): filesFolder
            members (array): A collection of membership records associated with the channel.
            messages (array): A collection of all the messages in the channel. A navigation property. Nullable.
            sharedWithTeams (array): A collection of teams with which a channel is shared.
            tabs (array): A collection of all the tabs in the channel. A navigation property.

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'createdDateTime': createdDateTime,
            'description': description,
            'displayName': displayName,
            'email': email,
            'isArchived': isArchived,
            'isFavoriteByDefault': isFavoriteByDefault,
            'membershipType': membershipType,
            'summary': summary,
            'tenantId': tenantId,
            'webUrl': webUrl,
            'allMembers': allMembers,
            'filesFolder': filesFolder,
            'members': members,
            'messages': messages,
            'sharedWithTeams': sharedWithTeams,
            'tabs': tabs,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def delete_group_channel(self, group_id: str, channel_id: str) -> Any:
        """
        Delete navigation property channels for groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def list_channel_members_by_groupid_channelid(self, group_id: str, channel_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        Get allMembers from groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/allMembers"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def create_group_team_channel(self, group_id: str, channel_id: str, id: Optional[str] = None, displayName: Optional[str] = None, roles: Optional[List[str]] = None, visibleHistoryStartDateTime: Optional[str] = None) -> Any:
        """
        Create new navigation property to allMembers for groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            id (string): The unique identifier for an entity. Read-only.
            displayName (string): The display name of the user.
            roles (array): The roles for that user. This property contains more qualifiers only when relevant - for example, if the member has owner privileges, the roles property contains owner as one of the values. Similarly, if the member is an in-tenant guest, the roles property contains guest as one of the values. A basic member shouldn't have any values specified in the roles property. An Out-of-tenant external member is assigned the owner role.
            visibleHistoryStartDateTime (string): The timestamp denoting how far back a conversation's history is shared with the conversation member. This property is settable only for members of a chat.

        Returns:
            Any: Created navigation property.

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'displayName': displayName,
            'roles': roles,
            'visibleHistoryStartDateTime': visibleHistoryStartDateTime,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/allMembers"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def get_channel_member_details(self, group_id: str, channel_id: str, conversationMember_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get allMembers from groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            conversationMember_id (string): conversationMember-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if conversationMember_id is None:
            raise ValueError("Missing required parameter 'conversationMember-id'.")
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/allMembers/{conversationMember_id}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_group_team_channel_member(self, group_id: str, channel_id: str, conversationMember_id: str, id: Optional[str] = None, displayName: Optional[str] = None, roles: Optional[List[str]] = None, visibleHistoryStartDateTime: Optional[str] = None) -> Any:
        """
        Update the navigation property allMembers in groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            conversationMember_id (string): conversationMember-id
            id (string): The unique identifier for an entity. Read-only.
            displayName (string): The display name of the user.
            roles (array): The roles for that user. This property contains more qualifiers only when relevant - for example, if the member has owner privileges, the roles property contains owner as one of the values. Similarly, if the member is an in-tenant guest, the roles property contains guest as one of the values. A basic member shouldn't have any values specified in the roles property. An Out-of-tenant external member is assigned the owner role.
            visibleHistoryStartDateTime (string): The timestamp denoting how far back a conversation's history is shared with the conversation member. This property is settable only for members of a chat.

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if conversationMember_id is None:
            raise ValueError("Missing required parameter 'conversationMember-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'displayName': displayName,
            'roles': roles,
            'visibleHistoryStartDateTime': visibleHistoryStartDateTime,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/allMembers/{conversationMember_id}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def delete_group_channel_member(self, group_id: str, channel_id: str, conversationMember_id: str) -> Any:
        """
        Delete navigation property allMembers for groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            conversationMember_id (string): conversationMember-id

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if conversationMember_id is None:
            raise ValueError("Missing required parameter 'conversationMember-id'.")
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/allMembers/{conversationMember_id}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def get_group_messages(self, group_id: str, channel_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        Get messages from groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/messages"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def create_group_channel_message(self, group_id: str, channel_id: str, id: Optional[str] = None, attachments: Optional[List[dict[str, dict[str, Any]]]] = None, body: Optional[dict[str, dict[str, Any]]] = None, channelIdentity: Optional[dict[str, dict[str, Any]]] = None, chatId: Optional[str] = None, createdDateTime: Optional[str] = None, deletedDateTime: Optional[str] = None, etag: Optional[str] = None, eventDetail: Optional[dict[str, dict[str, Any]]] = None, from_: Optional[Any] = None, importance: Optional[str] = None, lastEditedDateTime: Optional[str] = None, lastModifiedDateTime: Optional[str] = None, locale: Optional[str] = None, mentions: Optional[List[dict[str, dict[str, Any]]]] = None, messageHistory: Optional[List[dict[str, dict[str, Any]]]] = None, messageType: Optional[str] = None, policyViolation: Optional[dict[str, dict[str, Any]]] = None, reactions: Optional[List[dict[str, dict[str, Any]]]] = None, replyToId: Optional[str] = None, subject: Optional[str] = None, summary: Optional[str] = None, webUrl: Optional[str] = None, hostedContents: Optional[List[Any]] = None, replies: Optional[List[Any]] = None) -> Any:
        """
        Create new navigation property to messages for groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            id (string): The unique identifier for an entity. Read-only.
            attachments (array): References to attached objects like files, tabs, meetings etc.
            body (object): body
            channelIdentity (object): channelIdentity
            chatId (string): If the message was sent in a chat, represents the identity of the chat.
            createdDateTime (string): Timestamp of when the chat message was created.
            deletedDateTime (string): Read only. Timestamp at which the chat message was deleted, or null if not deleted.
            etag (string): Read-only. Version number of the chat message.
            eventDetail (object): eventDetail
            from_ (string): from
            importance (string): importance
            lastEditedDateTime (string): Read only. Timestamp when edits to the chat message were made. Triggers an 'Edited' flag in the Teams UI. If no edits are made the value is null.
            lastModifiedDateTime (string): Read only. Timestamp when the chat message is created (initial setting) or modified, including when a reaction is added or removed.
            locale (string): Locale of the chat message set by the client. Always set to en-us.
            mentions (array): List of entities mentioned in the chat message. Supported entities are: user, bot, team, channel, chat, and tag.
            messageHistory (array): List of activity history of a message item, including modification time and actions, such as reactionAdded, reactionRemoved, or reaction changes, on the message.
            messageType (string): messageType
            policyViolation (object): policyViolation
            reactions (array): Reactions for this chat message (for example, Like).
            replyToId (string): Read-only. ID of the parent chat message or root chat message of the thread. (Only applies to chat messages in channels, not chats.)
            subject (string): The subject of the chat message, in plaintext.
            summary (string): Summary text of the chat message that could be used for push notifications and summary views or fall back views. Only applies to channel chat messages, not chat messages in a chat.
            webUrl (string): Read-only. Link to the message in Microsoft Teams.
            hostedContents (array): Content in a message hosted by Microsoft Teams - for example, images or code snippets.
            replies (array): Replies for a specified message. Supports $expand for channel messages.

        Returns:
            Any: Created navigation property.

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'attachments': attachments,
            'body': body,
            'channelIdentity': channelIdentity,
            'chatId': chatId,
            'createdDateTime': createdDateTime,
            'deletedDateTime': deletedDateTime,
            'etag': etag,
            'eventDetail': eventDetail,
            'from': from_,
            'importance': importance,
            'lastEditedDateTime': lastEditedDateTime,
            'lastModifiedDateTime': lastModifiedDateTime,
            'locale': locale,
            'mentions': mentions,
            'messageHistory': messageHistory,
            'messageType': messageType,
            'policyViolation': policyViolation,
            'reactions': reactions,
            'replyToId': replyToId,
            'subject': subject,
            'summary': summary,
            'webUrl': webUrl,
            'hostedContents': hostedContents,
            'replies': replies,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/messages"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def get_group_channel_messages(self, group_id: str, channel_id: str, chatMessage_id: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get messages from groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/messages/{chatMessage_id}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_message(self, group_id: str, channel_id: str, chatMessage_id: str, id: Optional[str] = None, attachments: Optional[List[dict[str, dict[str, Any]]]] = None, body: Optional[dict[str, dict[str, Any]]] = None, channelIdentity: Optional[dict[str, dict[str, Any]]] = None, chatId: Optional[str] = None, createdDateTime: Optional[str] = None, deletedDateTime: Optional[str] = None, etag: Optional[str] = None, eventDetail: Optional[dict[str, dict[str, Any]]] = None, from_: Optional[Any] = None, importance: Optional[str] = None, lastEditedDateTime: Optional[str] = None, lastModifiedDateTime: Optional[str] = None, locale: Optional[str] = None, mentions: Optional[List[dict[str, dict[str, Any]]]] = None, messageHistory: Optional[List[dict[str, dict[str, Any]]]] = None, messageType: Optional[str] = None, policyViolation: Optional[dict[str, dict[str, Any]]] = None, reactions: Optional[List[dict[str, dict[str, Any]]]] = None, replyToId: Optional[str] = None, subject: Optional[str] = None, summary: Optional[str] = None, webUrl: Optional[str] = None, hostedContents: Optional[List[Any]] = None, replies: Optional[List[Any]] = None) -> Any:
        """
        Update the navigation property messages in groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id
            id (string): The unique identifier for an entity. Read-only.
            attachments (array): References to attached objects like files, tabs, meetings etc.
            body (object): body
            channelIdentity (object): channelIdentity
            chatId (string): If the message was sent in a chat, represents the identity of the chat.
            createdDateTime (string): Timestamp of when the chat message was created.
            deletedDateTime (string): Read only. Timestamp at which the chat message was deleted, or null if not deleted.
            etag (string): Read-only. Version number of the chat message.
            eventDetail (object): eventDetail
            from_ (string): from
            importance (string): importance
            lastEditedDateTime (string): Read only. Timestamp when edits to the chat message were made. Triggers an 'Edited' flag in the Teams UI. If no edits are made the value is null.
            lastModifiedDateTime (string): Read only. Timestamp when the chat message is created (initial setting) or modified, including when a reaction is added or removed.
            locale (string): Locale of the chat message set by the client. Always set to en-us.
            mentions (array): List of entities mentioned in the chat message. Supported entities are: user, bot, team, channel, chat, and tag.
            messageHistory (array): List of activity history of a message item, including modification time and actions, such as reactionAdded, reactionRemoved, or reaction changes, on the message.
            messageType (string): messageType
            policyViolation (object): policyViolation
            reactions (array): Reactions for this chat message (for example, Like).
            replyToId (string): Read-only. ID of the parent chat message or root chat message of the thread. (Only applies to chat messages in channels, not chats.)
            subject (string): The subject of the chat message, in plaintext.
            summary (string): Summary text of the chat message that could be used for push notifications and summary views or fall back views. Only applies to channel chat messages, not chat messages in a chat.
            webUrl (string): Read-only. Link to the message in Microsoft Teams.
            hostedContents (array): Content in a message hosted by Microsoft Teams - for example, images or code snippets.
            replies (array): Replies for a specified message. Supports $expand for channel messages.

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'attachments': attachments,
            'body': body,
            'channelIdentity': channelIdentity,
            'chatId': chatId,
            'createdDateTime': createdDateTime,
            'deletedDateTime': deletedDateTime,
            'etag': etag,
            'eventDetail': eventDetail,
            'from': from_,
            'importance': importance,
            'lastEditedDateTime': lastEditedDateTime,
            'lastModifiedDateTime': lastModifiedDateTime,
            'locale': locale,
            'mentions': mentions,
            'messageHistory': messageHistory,
            'messageType': messageType,
            'policyViolation': policyViolation,
            'reactions': reactions,
            'replyToId': replyToId,
            'subject': subject,
            'summary': summary,
            'webUrl': webUrl,
            'hostedContents': hostedContents,
            'replies': replies,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/messages/{chatMessage_id}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def delete_message_in_channel(self, group_id: str, channel_id: str, chatMessage_id: str) -> Any:
        """
        Delete navigation property messages for groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/messages/{chatMessage_id}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def get_chat_message_replies(self, group_id: str, channel_id: str, chatMessage_id: str, top: Optional[int] = None, skip: Optional[int] = None, search: Optional[str] = None, filter: Optional[str] = None, count: Optional[bool] = None, orderby: Optional[List[str]] = None, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> dict[str, Any]:
        """
        Get replies from groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id
            top (integer): Show only the first n items Example: '50'.
            skip (integer): Skip the first n items
            search (string): Search items by search phrases
            filter (string): Filter items by property values
            count (boolean): Include count of items
            orderby (array): Order items by property values
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            dict[str, Any]: Retrieved collection

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/messages/{chatMessage_id}/replies"
        query_params = {k: v for k, v in [('$top', top), ('$skip', skip), ('$search', search), ('$filter', filter), ('$count', count), ('$orderby', orderby), ('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def create_reply_in_message(self, group_id: str, channel_id: str, chatMessage_id: str, id: Optional[str] = None, attachments: Optional[List[dict[str, dict[str, Any]]]] = None, body: Optional[dict[str, dict[str, Any]]] = None, channelIdentity: Optional[dict[str, dict[str, Any]]] = None, chatId: Optional[str] = None, createdDateTime: Optional[str] = None, deletedDateTime: Optional[str] = None, etag: Optional[str] = None, eventDetail: Optional[dict[str, dict[str, Any]]] = None, from_: Optional[Any] = None, importance: Optional[str] = None, lastEditedDateTime: Optional[str] = None, lastModifiedDateTime: Optional[str] = None, locale: Optional[str] = None, mentions: Optional[List[dict[str, dict[str, Any]]]] = None, messageHistory: Optional[List[dict[str, dict[str, Any]]]] = None, messageType: Optional[str] = None, policyViolation: Optional[dict[str, dict[str, Any]]] = None, reactions: Optional[List[dict[str, dict[str, Any]]]] = None, replyToId: Optional[str] = None, subject: Optional[str] = None, summary: Optional[str] = None, webUrl: Optional[str] = None, hostedContents: Optional[List[Any]] = None, replies: Optional[List[Any]] = None) -> Any:
        """
        Create new navigation property to replies for groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id
            id (string): The unique identifier for an entity. Read-only.
            attachments (array): References to attached objects like files, tabs, meetings etc.
            body (object): body
            channelIdentity (object): channelIdentity
            chatId (string): If the message was sent in a chat, represents the identity of the chat.
            createdDateTime (string): Timestamp of when the chat message was created.
            deletedDateTime (string): Read only. Timestamp at which the chat message was deleted, or null if not deleted.
            etag (string): Read-only. Version number of the chat message.
            eventDetail (object): eventDetail
            from_ (string): from
            importance (string): importance
            lastEditedDateTime (string): Read only. Timestamp when edits to the chat message were made. Triggers an 'Edited' flag in the Teams UI. If no edits are made the value is null.
            lastModifiedDateTime (string): Read only. Timestamp when the chat message is created (initial setting) or modified, including when a reaction is added or removed.
            locale (string): Locale of the chat message set by the client. Always set to en-us.
            mentions (array): List of entities mentioned in the chat message. Supported entities are: user, bot, team, channel, chat, and tag.
            messageHistory (array): List of activity history of a message item, including modification time and actions, such as reactionAdded, reactionRemoved, or reaction changes, on the message.
            messageType (string): messageType
            policyViolation (object): policyViolation
            reactions (array): Reactions for this chat message (for example, Like).
            replyToId (string): Read-only. ID of the parent chat message or root chat message of the thread. (Only applies to chat messages in channels, not chats.)
            subject (string): The subject of the chat message, in plaintext.
            summary (string): Summary text of the chat message that could be used for push notifications and summary views or fall back views. Only applies to channel chat messages, not chat messages in a chat.
            webUrl (string): Read-only. Link to the message in Microsoft Teams.
            hostedContents (array): Content in a message hosted by Microsoft Teams - for example, images or code snippets.
            replies (array): Replies for a specified message. Supports $expand for channel messages.

        Returns:
            Any: Created navigation property.

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'attachments': attachments,
            'body': body,
            'channelIdentity': channelIdentity,
            'chatId': chatId,
            'createdDateTime': createdDateTime,
            'deletedDateTime': deletedDateTime,
            'etag': etag,
            'eventDetail': eventDetail,
            'from': from_,
            'importance': importance,
            'lastEditedDateTime': lastEditedDateTime,
            'lastModifiedDateTime': lastModifiedDateTime,
            'locale': locale,
            'mentions': mentions,
            'messageHistory': messageHistory,
            'messageType': messageType,
            'policyViolation': policyViolation,
            'reactions': reactions,
            'replyToId': replyToId,
            'subject': subject,
            'summary': summary,
            'webUrl': webUrl,
            'hostedContents': hostedContents,
            'replies': replies,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/messages/{chatMessage_id}/replies"
        query_params = {}
        return self._post_json(url, data=request_body_data, params=query_params, content_type='application/json')

    def get_reply_messages(self, group_id: str, channel_id: str, chatMessage_id: str, chatMessage_id1: str, select: Optional[List[str]] = None, expand: Optional[List[str]] = None) -> Any:
        """
        Get replies from groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id
            chatMessage_id1 (string): chatMessage-id1
            select (array): Select properties to be returned
            expand (array): Expand related entities

        Returns:
            Any: Retrieved navigation property

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        if chatMessage_id1 is None:
            raise ValueError("Missing required parameter 'chatMessage-id1'.")
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/messages/{chatMessage_id}/replies/{chatMessage_id1}"
        query_params = {k: v for k, v in [('$select', select), ('$expand', expand)] if v is not None}
        return self._get_json(url, params=query_params)

    def update_reply_message(self, group_id: str, channel_id: str, chatMessage_id: str, chatMessage_id1: str, id: Optional[str] = None, attachments: Optional[List[dict[str, dict[str, Any]]]] = None, body: Optional[dict[str, dict[str, Any]]] = None, channelIdentity: Optional[dict[str, dict[str, Any]]] = None, chatId: Optional[str] = None, createdDateTime: Optional[str] = None, deletedDateTime: Optional[str] = None, etag: Optional[str] = None, eventDetail: Optional[dict[str, dict[str, Any]]] = None, from_: Optional[Any] = None, importance: Optional[str] = None, lastEditedDateTime: Optional[str] = None, lastModifiedDateTime: Optional[str] = None, locale: Optional[str] = None, mentions: Optional[List[dict[str, dict[str, Any]]]] = None, messageHistory: Optional[List[dict[str, dict[str, Any]]]] = None, messageType: Optional[str] = None, policyViolation: Optional[dict[str, dict[str, Any]]] = None, reactions: Optional[List[dict[str, dict[str, Any]]]] = None, replyToId: Optional[str] = None, subject: Optional[str] = None, summary: Optional[str] = None, webUrl: Optional[str] = None, hostedContents: Optional[List[Any]] = None, replies: Optional[List[Any]] = None) -> Any:
        """
        Update the navigation property replies in groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id
            chatMessage_id1 (string): chatMessage-id1
            id (string): The unique identifier for an entity. Read-only.
            attachments (array): References to attached objects like files, tabs, meetings etc.
            body (object): body
            channelIdentity (object): channelIdentity
            chatId (string): If the message was sent in a chat, represents the identity of the chat.
            createdDateTime (string): Timestamp of when the chat message was created.
            deletedDateTime (string): Read only. Timestamp at which the chat message was deleted, or null if not deleted.
            etag (string): Read-only. Version number of the chat message.
            eventDetail (object): eventDetail
            from_ (string): from
            importance (string): importance
            lastEditedDateTime (string): Read only. Timestamp when edits to the chat message were made. Triggers an 'Edited' flag in the Teams UI. If no edits are made the value is null.
            lastModifiedDateTime (string): Read only. Timestamp when the chat message is created (initial setting) or modified, including when a reaction is added or removed.
            locale (string): Locale of the chat message set by the client. Always set to en-us.
            mentions (array): List of entities mentioned in the chat message. Supported entities are: user, bot, team, channel, chat, and tag.
            messageHistory (array): List of activity history of a message item, including modification time and actions, such as reactionAdded, reactionRemoved, or reaction changes, on the message.
            messageType (string): messageType
            policyViolation (object): policyViolation
            reactions (array): Reactions for this chat message (for example, Like).
            replyToId (string): Read-only. ID of the parent chat message or root chat message of the thread. (Only applies to chat messages in channels, not chats.)
            subject (string): The subject of the chat message, in plaintext.
            summary (string): Summary text of the chat message that could be used for push notifications and summary views or fall back views. Only applies to channel chat messages, not chat messages in a chat.
            webUrl (string): Read-only. Link to the message in Microsoft Teams.
            hostedContents (array): Content in a message hosted by Microsoft Teams - for example, images or code snippets.
            replies (array): Replies for a specified message. Supports $expand for channel messages.

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        if chatMessage_id1 is None:
            raise ValueError("Missing required parameter 'chatMessage-id1'.")
        request_body_data = None
        request_body_data = {
            'id': id,
            'attachments': attachments,
            'body': body,
            'channelIdentity': channelIdentity,
            'chatId': chatId,
            'createdDateTime': createdDateTime,
            'deletedDateTime': deletedDateTime,
            'etag': etag,
            'eventDetail': eventDetail,
            'from': from_,
            'importance': importance,
            'lastEditedDateTime': lastEditedDateTime,
            'lastModifiedDateTime': lastModifiedDateTime,
            'locale': locale,
            'mentions': mentions,
            'messageHistory': messageHistory,
            'messageType': messageType,
            'policyViolation': policyViolation,
            'reactions': reactions,
            'replyToId': replyToId,
            'subject': subject,
            'summary': summary,
            'webUrl': webUrl,
            'hostedContents': hostedContents,
            'replies': replies,
        }
        request_body_data = {k: v for k, v in request_body_data.items() if v is not None}
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/messages/{chatMessage_id}/replies/{chatMessage_id1}"
        query_params = {}
        return self._patch_json(url, data=request_body_data, params=query_params)

    def delete_channel_message_reply(self, group_id: str, channel_id: str, chatMessage_id: str, chatMessage_id1: str) -> Any:
        """
        Delete navigation property replies for groups

        Args:
            group_id (string): group-id
            channel_id (string): channel-id
            chatMessage_id (string): chatMessage-id
            chatMessage_id1 (string): chatMessage-id1

        Returns:
            Any: Success

        Raises:
            HTTPStatusError: Raised when the API request fails with detailed error information including status code and response body.

        Tags:
            groups.team
        """
        if group_id is None:
            raise ValueError("Missing required parameter 'group-id'.")
        if channel_id is None:
            raise ValueError("Missing required parameter 'channel-id'.")
        if chatMessage_id is None:
            raise ValueError("Missing required parameter 'chatMessage-id'.")
        if chatMessage_id1 is None:
            raise ValueError("Missing required parameter 'chatMessage-id1'.")
        url = f"{self.base_url}/groups/{group_id}/team/channels/{channel_id}/messages/{chatMessage_id}/replies/{chatMessage_id1}"
        query_params = {}
        return self._delete_json(url, params=query_params)

    def list_tools(self):
        return [
            self.list_teams,
            self.create_team,
            self.get_team_info,
            self.update_team,
            self.delete_team_entity,
            self.list_channels_for_team,
            self.create_team_channel,
            self.get_team_channel_info,
            self.update_channel,
            self.delete_channel,
            self.get_team_members_list,
            self.add_member_to_team,
            self.list_channel_messages_by_id,
            self.send_chat_message,
            self.list_all_team_channel_members,
            self.create_team_channel_members,
            self.get_team_channel_members_details,
            self.update_conversation_member_in_team,
            self.delete_team_channel_member,
            self.list_channel_members_by_team_and_channel,
            self.add_member_to_channel_teamwise,
            self.get_channel_member,
            self.update_channel_member_by_id,
            self.delete_conversation_member,
            self.get_chat_message,
            self.update_chat_message_by_team_channel,
            self.delete_team_channel_message,
            self.get_replies,
            self.create_channel_message_reply,
            self.get_chat_message_reply,
            self.update_message_reply,
            self.delete_team_channel_message_reply,
            self.list_channel_shared_teams,
            self.share_channel_with_team,
            self.get_shared_teams_channels_info,
            self.update_shared_with_team_info,
            self.delete_shared_team_channel_link,
            self.list_channel_allowed_members,
            self.get_channel_allowed_member_by_id,
            self.list_chats,
            self.create_chat_operation,
            self.get_chat,
            self.update_chat_details,
            self.delete_chat_by_id,
            self.list_chat_members,
            self.add_member_to_chat,
            self.get_conversation_member,
            self.update_chat_member,
            self.remove_conversation_member,
            self.list_chat_messages,
            self.post_chat_message,
            self.get_chat_message_detail,
            self.update_chat_messages,
            self.delete_chat_messages,
            self.read_chat_replies,
            self.create_chat_reply,
            self.get_chat_replies,
            self.update_chat_replies,
            self.delete_chat_reply,
            self.get_group_team,
            self.create_team_from_group,
            self.delete_group_team,
            self.fetch_groups_team_all_channels,
            self.get_group_team_all_channels,
            self.get_group_channels,
            self.update_group_channels,
            self.delete_group_channel,
            self.list_channel_members_by_groupid_channelid,
            self.create_group_team_channel,
            self.get_channel_member_details,
            self.update_group_team_channel_member,
            self.delete_group_channel_member,
            self.get_group_messages,
            self.create_group_channel_message,
            self.get_group_channel_messages,
            self.update_message,
            self.delete_message_in_channel,
            self.get_chat_message_replies,
            self.create_reply_in_message,
            self.get_reply_messages,
            self.update_reply_message,
            self.delete_channel_message_reply
        ]
