from dataclasses import asdict

from SpiritGuard.model.user import User

USERS_NODE = 'users'
PENDING_INVITATIONS_NODE = 'pending_invitations'
SENT_INVITATIONS_NODE = 'sent_invitations'


class DatabaseService:

    def __init__(self, db) -> None:
        super().__init__()
        self.db = db

    def create_user(self, user: User):
        """
        Registers a user in firebase db.
        """
        self.db.child(USERS_NODE).child(user.identifier).set(asdict(user))

    def send_friend_invitation(self, sender_id, receiver_id):
        """
            Sends friendship invitation from one friend to another
            :param sender_id - id of a user that send an invitation for another user
            :param friend_to_add_id - id of an invitation receiver
        """
        self._update_receiver_pending_invitations(receiver_id, sender_id)
        self._update_sender_sent_invitations(sender_id, receiver_id)

    def _update_receiver_pending_invitations(self, receiver_id, sender_id):
        receiver_pending_invitations = self.db.child(USERS_NODE).child(receiver_id).child(
            PENDING_INVITATIONS_NODE).get().val()
        receiver_pending_invitations.append(sender_id)
        self.db.child(USERS_NODE).child(receiver_id).child(PENDING_INVITATIONS_NODE).set(receiver_pending_invitations)

    def _update_sender_sent_invitations(self, sender_id, receiver_id):
        sender_sent_invitations = self.db.child(USERS_NODE).child(sender_id).child(SENT_INVITATIONS_NODE).get().val()
        sender_sent_invitations.append(receiver_id)
        self.db.child(USERS_NODE).child(sender_id).child(SENT_INVITATIONS_NODE).set(sender_sent_invitations)

    def accept_friend_invitation(self, receiver_id, sender_id):
        # remove from sender sent
        # remove from receiver pending
        # add receiver to sender friends
        # add sender to receiver friends
        """
        Accepts friend invitation from sender to receiver.

        - removes receiver from sender's sent_notifications
        - removes sender from receiver's pending_notifications
        - adds both receiver and sender as each friends

        :param receiver_id - id of user that  accepts an invitation
        :param sender_id - id of user that sends invitation
        :return:
        """
        
