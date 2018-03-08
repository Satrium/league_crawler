from sqlalchemy import Table, Column, Integer, String, BigInteger, Boolean, ForeignKey, ForeignKeyConstraint, Numeric

from cassiopeia_sqlstore.common import metadata, SQLBaseObject, map_object

class SQLParticipantAdditional(SQLBaseObject):
    _dto_type = None
    _table = Table("match_participant_additional", metadata,
                    Column("platformId", String(5), primary_key=True),
                    Column("gameId", BigInteger, primary_key=True),
                    Column("participantId", Integer, primary_key=True),
                    Column("division", Integer),
                    Column("tier", Integer),
                    Column("champ_level", Integer),
                    Column("champ_points", Integer),
                    ForeignKeyConstraint(
                        ["platformId","gameId","participantId"],
                        ["match_participant.match_platformId","match_participant.match_gameId","match_participant.participantId"]
                    ))

map_object(SQLParticipantAdditional)