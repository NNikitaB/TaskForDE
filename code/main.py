import os
from fastapi import FastAPI
from sqlalchemy import create_engine, select, text
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import Session
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from classDTO import my_parse_json_to_dto
from classDB import Base, convert_dto_to_class_db, Missions, Rockets, Launches

user_bd = os.getenv('POSTGRES_USER')
pass_bd = os.getenv('POSTGRES_PASSWORD')
host_bd = os.getenv('POSTGRES_DB_CONTAINER')
port_bd = os.getenv('PORT_TMP')
name_bd = os.getenv('POSTGRES_DB')
url = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(user_bd, pass_bd, host_bd, port_bd, name_bd)
query_ql = """
query Query {
  rockets {
    name
    wikipedia
    description
    id
  }
  launches {
    rocket {
      rocket {
        id
      }
    }
    mission_id
    details
    launch_date_utc
    mission_name
    id
  }
  missions {
    id
    name
  }
}
"""
#url="sqlite:////teat.db"
#engine = create_engine(url, echo=True)
#Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/fill_db/")
def fill_db():
    """
    fills tables in to the db
    1.Drop all tables stored in this metadata
    2.Create all tables stored in this metadata
    3.Populates all tables with data
    """
    engine = create_engine(url, echo=True)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://spacex-production.up.railway.app/")
    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)
    # Use a breakpoint in the code line below to debug your script.
    query = gql(query_ql)
    # Execute the query on the transport
    result = client.execute(query)
    # Parse JSON to DTO Classes
    ls_missions, ls_rockets, ls_launches = my_parse_json_to_dto(result)
    with Session(engine) as session:
        # convert DTO Classes to SQLAlchemy classes
        rockets, launches = convert_dto_to_class_db(ls_missions, ls_rockets, ls_launches)
        # Populates all tables
        session.add_all(rockets)
        session.add_all(launches)
        # commit changes
        session.commit()
        return {"massage":"All ok"}


@app.get("/get_count/")
def get_count():
    """
    Счиает кол-во ракет,миссий,запусковb и всего
    :return count are missions,rockets,launches,all:
    """
    engine = create_engine(url, echo=True)
    Base.metadata.create_all(bind=engine)
    if not database_exists(engine.url):
        raise "DB not created"
    with Session(engine) as session:
        count_missions = session.scalars(select(Missions)).all()
        count_rockets = session.scalars(select(Rockets)).all()
        count_launches = session.scalars(select(Launches)).all()
        count_missions, count_rockets, count_launches = len(count_missions), len(count_rockets), len(count_launches)
        return {"count_missions": count_missions,
                "count_rockets": count_rockets,
                "count_launches": count_launches,
                "all": count_launches+count_rockets+count_missions
                }

