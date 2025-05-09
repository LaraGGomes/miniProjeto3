from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint, Table
from sqlalchemy.orm import relationship
from .database import Base

# Modelos SQLAlchemy
User_Post_association = Table(
    'user_post', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('post_id', Integer, ForeignKey('posts.id')),
)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    posts = relationship('Post', secondary=User_Post_association, back_populates='users')
    

    
class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String,ForeignKey('users.username'))
    users = relationship('User', secondary=User_Post_association, back_populates='posts')
    
User.posts = relationship('Post', secondary=User_Post_association, back_populates='users')