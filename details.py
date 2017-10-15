from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, UserData
engine = create_engine('sqlite:///catalogDB.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
User1 = UserData(name="Priyanka Nalawade", email="priyankanalawade108@gmail.com")
session.add(User1)
session.commit()
session.query(UserData).all()
User2 = UserData(name="Priyanka Nalawade", email="piyu1081991@gmail.com")
session.add(User2)
session.commit()
session.query(UserData).all()
myfirstcategory = Category(user_id=1, name="Cat1")
session.add(myfirstcategory)
session.commit()
session.query(Category).all()
mysecondcategory = Category(user_id=1, name="Cat2")
session.add(mysecondcategory)
session.commit()
session.query(Category).all()
mythirdcategory = Category(user_id=2, name="Cat3")
session.add(mythirdcategory)
session.commit()
session.query(Category).all()
myfourthcategory = Category(user_id=2, name="Cat4")
session.add(myfourthcategory)
session.commit()
session.query(Category).all()
firstcatfirstitem = Item(
    user_id=1,
    title="firstcatfirstitem",
    description="this is firstcatfirstitem ",
    category=myfirstcategory)
session.add(firstcatfirstitem)
session.commit()
session.query(Item).all()
firstcatseconditem = Item(
    user_id=1,
    title="firstcatseconditem",
    description="this is firstcatseconditem",
    category=myfirstcategory)
session.add(firstcatseconditem)
session.commit()
session.query(Item).all()
firstcatthirdtitem = Item(
    user_id=1,
    title="firstcatthirditem",
    description="this is firstcatthirditem ",
    category=myfirstcategory)
session.add(firstcatthirdtitem)
session.commit()
session.query(Item).all()
secondcatfirstitem = Item(
    user_id=1,
    title="secondcatfirstitem ",
    description="this is firstcatfirstitem ",
    category=mysecondcategory)
session.add(secondcatfirstitem)
session.commit()
session.query(Item).all()
secondcatseconditem = Item(
    user_id=1,
    title="secondcatseconditem ",
    description="this is secondcatseconditem ",
    category=mysecondcategory)
session.add(secondcatseconditem)
session.commit()
session.query(Item).all()
secondcatthirditem = Item(
    user_id=1,
    title="secondcatthirditem ",
    description="this is secondcatthirditem ",
    category=mysecondcategory)
session.add(secondcatthirditem)
session.commit()
session.query(Item).all()
thirdcatfirstitem = Item(
    user_id=2,
    title="thirdcatfirstitem ",
    description="this is thirdcatfirstitem ",
    category=mythirdcategory)
session.add(thirdcatfirstitem)
session.commit()
session.query(Item).all()
thirdcatseconditem = Item(
    user_id=2,
    title="thirdcatseconditem ",
    description="this is thirdcatseconditem ",
    category=mythirdcategory)
session.add(thirdcatseconditem)
session.commit()
session.query(Item).all()
thirdcatthirditem = Item(
    user_id=2,
    title="thirdcatthirditem ",
    description="this is thirdcatthirditem ",
    category=mythirdcategory)
session.add(thirdcatthirditem)
session.commit()
session.query(Item).all()
fourthcatfirstitem = Item(
    user_id=2,
    title="fourthcatfirstitem ",
    description="this is fourthcatfirstitem ",
    category=myfourthcategory)
session.add(fourthcatfirstitem)
session.commit()
session.query(Item).all()
fourthcatseconditem = Item(
    user_id=2,
    title="fourthcatseconditem ",
    description="this is fourthcatseconditem ",
    category=myfourthcategory)
session.add(fourthcatseconditem)
session.commit()
session.query(Item).all()
fourthcatthirditem = Item(
    user_id=2,
    title="fourthcatthirditem ",
    description="this is fourthcatthirditem ",
    category=myfourthcategory)
session.add(thirdcatthirditem)
session.commit()
session.query(Item).all()
