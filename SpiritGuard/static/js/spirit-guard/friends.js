const friendsState = {
    visible: false
};

function toggleFriendsList(friendsElem) {
    friendsState.visible ? friendsElem.hide() : friendsElem.show();
    friendsState.visible = !friendsState.visible
}

$(document).ready(() => {
    const friendsList = $('.fp');
    const friendsButton = $('#friends-btn');
    friendsList.hide();
    friendsButton.click((_) => toggleFriendsList(friendsList));
});