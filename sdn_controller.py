from sdn_rules import install_rule, remove_rule, show_rules


def main():
    while True:
        print("\n========== SDN CONTROLLER ==========")
        print("1. Block a site")
        print("2. Allow a site")
        print("3. Remove a rule")
        print("4. Show rules")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            site = input("Enter site/message to block: ")
            install_rule(site, "BLOCK")

        elif choice == "2":
            site = input("Enter site/message to allow: ")
            install_rule(site, "ALLOW")

        elif choice == "3":
            site = input("Enter site/message whose rule should be removed: ")
            remove_rule(site)

        elif choice == "4":
            show_rules()

        elif choice == "5":
            print("SDN Controller stopped.")
            break

        else:
            print("Invalid choice. Enter 1-5.")


if __name__ == "__main__":
    main()
