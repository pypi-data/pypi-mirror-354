import os
import pyshorteners

# Clear the terminal screen
os.system('clear' if os.name == 'posix' else 'cls')

# Function to create a short URL using TinyURL
def create_short_url(long_url):
    try:
        s = pyshorteners.Shortener()
        s.tinyurl.timeout = 10  
        short_url = s.tinyurl.short(long_url)
        return short_url
    except Exception as e:
        return f"\033[1;31m[ERROR]\033[0m {e}"

# Main program logic
def main():
    while True:
        print("\n\033[1;33m⚡ Choose an option:\033[0m")
        print(" \033[1;32m[1]\033[0m Shorten a single URL")
        print(" \033[1;32m[2]\033[0m Shorten multiple URLs from a file")
        print(" \033[1;32m[3]\033[0m Shorten URLs from multiple files")
        print(" \033[1;32m[4]\033[0m Exit")

        choice = input("\n\033[1;33mEnter your choice (1–4):\033[1;37m ")

        if choice == '4':
            print("\033[1;37m👋 Exiting the program. Goodbye!\033[0m")
            break

        elif choice == '1':
            long_url = input("\n\033[1;33m🔗 Enter the long URL:\033[0m \033[1;37m")
            short_url = create_short_url(long_url)
            print(f"\033[1;34m✅ Shortened URL:\033[1;32m {short_url}\033[0m")

        elif choice == '2':
            file_path = input("\n\033[1;33m📂 Enter path to the file with URLs:\033[0m \033[1;37m")
            try:
                with open(file_path, 'r') as file:
                    urls = file.readlines()

                with open('shortened_urls.txt', 'w') as output_file:
                    for url in urls:
                        url = url.strip()
                        if url:
                            short_url = create_short_url(url)
                            output_file.write(short_url + '\n')
                            print(f"\033[1;34m✅ {url} →\033[1;32m {short_url}\033[0m")

                print("\n\033[1;32m📁 All shortened URLs saved to 'shortened_urls.txt'\033[0m")
            except Exception as e:
                print(f"\033[1;31m[ERROR] File error:\033[0m {e}")

        elif choice == '3':
            file_list = input("\n\033[1;33m📂 Enter paths to the files (comma-separated):\033[0m \033[1;37m")
            file_paths = [f.strip() for f in file_list.split(",") if f.strip()]
            for file_path in file_paths:
                try:
                    with open(file_path, 'r') as file:
                        urls = file.readlines()

                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    output_file_name = f"{base_name}_shortened.txt"

                    with open(output_file_name, 'w') as output_file:
                        for url in urls:
                            url = url.strip()
                            if url:
                                short_url = create_short_url(url)
                                output_file.write(short_url + '\n')
                                print(f"\033[1;34m✅ {url} →\033[1;32m {short_url}\033[0m")

                    print(f"\n\033[1;32m📁 Output saved to '{output_file_name}'\033[0m")
                except Exception as e:
                    print(f"\033[1;31m[ERROR] Could not process file '{file_path}':\033[0m {e}")
        else:
            print("\033[1;31m❌ Invalid choice. Please select 1, 2, 3, or 4.\033[0m")

# Run the main function
if __name__ == "__main__":
    main()
