from sqlalchemy import event
from lecopain.app import db
from lecopain.dao.models import Stat

from datetime import datetime

@event.listens_for(db.session, 'before_commit')
def receive_after_commit(session):
    stat = Stat.query.get_or_404(1)
    stat.updated_at = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')
