class SensitiveInfo:
    def __init__(self):
        self.users = ['nick', 'tom', 'ben', 'mike']

    def read(self):
        print(f"There are {len(self.users)} users: {' '.join(self.users)}")

    def add(self, user):
        self.users.append(user)
        print(f'Added user {user}')

class ProxyInfo:
    """
    A protection proxy that uses dynamic attributes to forward
    all calls to the underlying SensitiveInfo, except for 'add',
    which requires a secret.
    """
    def __init__(self):
        self._secret = '0xdeadbeef'
        self._protected = SensitiveInfo()

    def __getattr__(self, name):
        # Dynamically forward unknown attribute accesses to the protected object
        return getattr(self._protected, name)

    def add(self, user):
        sec = input('what is the secret? ')
        if sec == self._secret:
            self._protected.add(user)
        else:
            print("Wrong secret!")

def main():
    info = ProxyInfo()
    while True:
        print('1. read list | 2. add user | 3. quit')
        choice = input('choose option: ')
        if choice == '1':
            info.read()  # calling read() is forwarded to SensitiveInfo via __getattr__
        elif choice == '2':
            user = input('username: ')
            info.add(user)  # triggers the overridden add() that requires secret
        elif choice == '3':
            break
        else:
            print(f'Unknown option: {choice}')

if __name__ == '__main__':
    main()
