import praw
import pandas as pd
import os


def main():
    titles = []
    upvotes = []
    comment_count = []
    links = []
    # Add your own authenticator here 
    reddit = praw.Reddit(client_id="",
                         client_secret="",
                         user_agent="")

    print("Enter 1 to scrape a subreddit or 2 to parse a CSV file of a scrapped search term")
    selection = int(input())
    # Select Option
    while selection != 1 and selection != 2:
        print("Enter 1 to scrape a subreddit or 2 to parse a CSV file of a scrapped search term")
        selection = int(input())

    # Search and Scrape
    if selection == 1:
        # Get a subreddit in the form of its name. Example LivestreamFail
        subreddit = input("Subreddit: \n")
        # Get a search term here
        topic = input("Title contains: \n")
        for submission in reddit.subreddit(subreddit).top(limit=1000, time_filter="year"):
            if topic in submission.title:
                titles.append(submission.title)
                upvotes.append(submission.score)
                comment_count.append(submission.num_comments)
                # Here, produce a link that leads directly to the submission post
                links.append("https://www.reddit.com" + submission.permalink)
        # Transform collected Data into a Pandas DataFrame
        df = pd.DataFrame({"Titles": titles,
                           "Upvotes": upvotes,
                           "# of Comments": comment_count,
                           "Links": links})
        # Write to CSV
        df.to_csv("csvs\\" + topic + ".csv", index=False)
    # Parse CSV
    else:
        num_files = 0
        csv_files = []
        cwd = os.getcwd() + "\csvs"
        print(cwd)
        # Select a CSV file to read and print
        for root, dirs, files in os.walk(cwd):
            for file in files:
                if file.endswith('.csv'):
                    print(str(num_files) + " - " + file)
                    csv_files.append(file)
                    num_files += 1

        print("Enter a number that corresponds to a file name displayed [0 - " + str(num_files - 1) + "]")
        selection = int(input())
        while selection <= 0 or selection >= num_files:
            print("Enter a number that corresponds to a file name displayed [0 - " + str(num_files - 1) + "]")
            selection = int(input())

        df = pd.read_csv("csvs\\" + csv_files[selection])
        print(df.to_string())


if __name__ == "__main__":
    main()
