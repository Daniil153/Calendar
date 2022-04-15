def find_user_by_login(login):
    for user in list_users:
        if user.mail == login:
            return user
    return User("NoUser", 'NoUser', 'NoUser', 'NoUser')


def parse_partisipants(s):
    return [find_user_by_login(i.strip(',')) for i in s.split(' ')]
