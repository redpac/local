ALTER TABLE banios.users
ADD CONSTRAINT UQ_Usuarios_Username UNIQUE (username);

CREATE TABLE [banios].[channels] (
    [id]   INT          IDENTITY (1, 1) NOT NULL,
    [name] VARCHAR (50) NOT NULL,
    [owner_id] INT NOT NULL,
    CONSTRAINT [PK_channels] PRIMARY KEY CLUSTERED ([id] ASC),
    CONSTRAINT UQ_Canales_name UNIQUE(name)
);

CREATE TABLE [banios].[channels_users] (
    [channel_id] INT NOT NULL,
    [user_id]    INT NOT NULL
);

CREATE TABLE [banios].[groups] (
    [id]   INT          IDENTITY (1, 1) NOT NULL,
    [name] VARCHAR (50) NOT NULL,
    CONSTRAINT [PK_groups] PRIMARY KEY CLUSTERED ([id] ASC),
    CONSTRAINT UQ_Grupos_name UNIQUE(name)
);

CREATE TABLE [banios].[groups_users] (
    [group_id] INT NOT NULL,
    [user_id]  INT NOT NULL
);

CREATE TABLE [banios].[private-chats] (
    [id]     INT IDENTITY (1, 1) NOT NULL,
    [user_1] INT NOT NULL,
    [user_2] INT NOT NULL,
    CONSTRAINT [PK_private-chats] PRIMARY KEY CLUSTERED ([id] ASC)
);
CREATE TABLE [banios].[public] (
    [id]        INT          IDENTITY (1, 1) NOT NULL,
    [sender] INT          NOT NULL,
    [content]   VARCHAR (50) NOT NULL,
    CONSTRAINT [PK_public] PRIMARY KEY CLUSTERED ([id] ASC)
);

CREATE TABLE [banios].[private_messages] (
    [id]      INT          IDENTITY (1, 1) NOT NULL,
    [chat_id] INT          NOT NULL,
    [sender_id] INT        NOT NULL,
    [content] VARCHAR (50) NOT NULL,
    CONSTRAINT [PK_private_messages] PRIMARY KEY CLUSTERED ([id] ASC)
);

CREATE TABLE [banios].[group_messages] (
    [id]       INT          IDENTITY (1, 1) NOT NULL,
    [group_id] INT          NOT NULL,
    [sender_id] INT         NOT NULL,
    [content]  VARCHAR (50) NOT NULL,
    CONSTRAINT [PK_group_messages] PRIMARY KEY CLUSTERED ([id] ASC)
);

CREATE TABLE [banios].[channel_messages] (
    [id]         INT          IDENTITY (1, 1) NOT NULL,
    [channel_id] INT          NOT NULL,
    [sender_id]  INT          NOT NULL,
    [content]    VARCHAR (50) NOT NULL,
    CONSTRAINT [PK_channel_messages] PRIMARY KEY CLUSTERED ([id] ASC)
);