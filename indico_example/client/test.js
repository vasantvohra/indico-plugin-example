import {showUserSearch, showGroupSearch} from 'indico/react/components/principals/imperative';

document.addEventListener('DOMContentLoaded', () => {
    const register_user = document.querySelector('#indico-user-to-add')
    register_user.addEventListener('click', async () => {
        const user = await showUserSearch({
            withExternalUsers: true,
            single: true,
            alwaysConfirm: true,
        });
        if (user) {
            alert(JSON.stringify(user));
        }
    })
})

document.addEventListener('DOMContentLoaded', () => {
    const register_group = document.querySelector('#indico-group-to-add')
    register_group.addEventListener('click', async () => {
        const groups = await showGroupSearch();
        if (groups) {
            alert(JSON.stringify(groups));
        }
    })
})