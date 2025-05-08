from sqlmodel import Field, SQLModel

class users(SQLModel, table= True):
    users_id: str = Field(default=None, primary_key=True)
    senha:    str

class posts(SQLModel, table= True):
    post_id:  int = Field(default=None, primary_key=True)
    post:     str
    users_id: str = Field(foreign_key="users.users_id")

class interaction(SQLModel, table= True):
    post:     int = Field(foreign_key="posts.post_id")
    users:    str = Field(foreign_key="users.users_id")