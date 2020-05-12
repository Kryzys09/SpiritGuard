from dataclasses import asdict

from SpiritGuard.model.user import User

USERS_NODE = 'users'
PENDING_INVITATIONS_NODE = 'pending_invitations'
SENT_INVITATIONS_NODE = 'sent_invitations'
FRIENDS_NODE = 'friends'


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
        receiver_pending_invitations = self._get_user_node(receiver_id, PENDING_INVITATIONS_NODE)
        receiver_pending_invitations.append(sender_id)
        self._post_user_node(receiver_id, PENDING_INVITATIONS_NODE, receiver_pending_invitations)

    def _update_sender_sent_invitations(self, sender_id, receiver_id):
        sender_sent_invitations = self._get_user_node(sender_id, SENT_INVITATIONS_NODE)
        sender_sent_invitations.append(receiver_id)
        self._post_user_node(sender_id, SENT_INVITATIONS_NODE, sender_sent_invitations)

    def accept_friend_invitation(self, receiver_id, sender_id):
        """
        Accepts friend invitation from sender to receiver.

        - removes receiver from sender's sent_notifications
        - removes sender from receiver's pending_notifications
        - adds both receiver and sender as each friends

        :param receiver_id - id of user that  accepts an invitation
        :param sender_id - id of user that sends invitation
        """
        self._remove_from_user_collection(sender_id, SENT_INVITATIONS_NODE, receiver_id)
        self._remove_from_user_collection(receiver_id, PENDING_INVITATIONS_NODE, sender_id)
        self._befriend_two_users(receiver_id, sender_id)

    def decline_friend_invitation(self, receiver_id, sender_id):
        """
        Declines friend invitation send from sender to receiver

        removes ids of both users from corresponding sent_notifications and pending_notifications lists
        """
        self._remove_from_user_collection(sender_id, SENT_INVITATIONS_NODE, receiver_id)
        self._remove_from_user_collection(receiver_id, PENDING_INVITATIONS_NODE, sender_id)

    def _befriend_two_users(self, first_id, second_id):
        first_friends = self._get_user_node(first_id, FRIENDS_NODE)
        second_friends = self._get_user_node(second_id, FRIENDS_NODE)
        first_friends.append(second_id)
        second_friends.append(first_id)
        self._post_user_node(first_id, FRIENDS_NODE, first_friends)
        self._post_user_node(second_id, FRIENDS_NODE, second_friends)

    def _get_user_node(self, user_id, node_name):
        return self.db.child(USERS_NODE).child(user_id).child(node_name).get().val()

    def _post_user_node(self, user_id, node_name, update_object):
        self.db.child(USERS_NODE).child(user_id).child(node_name).set(update_object)

    def _remove_from_user_collection(self, user_id, collection_name, rem_obj):
        collection = self.db.child(USERS_NODE).child(user_id).child(collection_name)
        collection.remove(rem_obj)
        self.db.child(USERS_NODE).child(user_id).child(collection_name).set(collection)
