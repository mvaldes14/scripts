import os
import re
from collections import defaultdict
from datetime import datetime
import yaml

def generate_grouped_blog_index(input_directory, base_url, output_filename="index.md"):
    """
    Iterates over Markdown files in a directory, extracts date and title from frontmatter,
    and generates a new 'index.md' file grouped by year and month, with custom blog URLs.

    Args:
        input_directory (str): The path to the directory containing Markdown files (your blog posts).
        base_url (str): The base URL of your blog (e.g., "https://yourblog.com/posts/").
        output_filename (str): The name of the output Markdown file (default: "index.md").
    """

    # Dictionary to store files grouped by YYYY-MM string
    # Key: "YYYY-MM" string, Value: List of (title, permalink, original_date_for_sorting) tuples
    files_by_month = defaultdict(list)

    # Regex to find the frontmatter block
    frontmatter_regex = re.compile(r"(?s)^---\s*\n(.*?)\n---\s*\n")

    for root, _, files in os.walk(input_directory):
        for filename in files:
            if filename.endswith(".md"):
                filepath = os.path.join(root, filename)
                prefix =  root.split("/")[-1]
                title = None
                file_date = None
                clean_filename = filename.split(".")[0]

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                        match = frontmatter_regex.match(content)
                        if match:
                            frontmatter_str = match.group(1)
                            try:
                                frontmatter = yaml.safe_load(frontmatter_str)
                                if frontmatter:
                                    date_value = frontmatter.get('date')
                                    title = frontmatter.get('title')
                                    if date_value:
                                        try:
                                            file_date = datetime.strptime(str(date_value), "%Y-%m-%d").date()
                                        except ValueError:
                                            print(f"Warning: Could not parse date '{date_value}' from frontmatter in {filepath}. Expected YYYY-MM-DD. Skipping file.")
                                            continue
                                    else:
                                        print(f"Warning: 'date' not found in frontmatter for {filepath}. Skipping file.")
                                        continue
                                else:
                                    print(f"Warning: Empty frontmatter in {filepath}. Skipping file.")
                                    continue
                            except yaml.YAMLError as e:
                                print(f"Warning: Could not parse YAML frontmatter in {filepath}. Error: {e}. Skipping file.")
                                continue
                        else:
                            print(f"Warning: No valid frontmatter found at the start of {filepath}. Skipping file.")
                            continue

                    if file_date:
                        month_key = file_date.strftime('%Y-%m')
                        permalink = f"{base_url}/{prefix}/{clean_filename}"
                        files_by_month[month_key].append((title, permalink, file_date))

                except Exception as e:
                    print(f"Error processing file {filepath}: {e}")
                    continue

    # Sort months in descending order (most recent month first)
    sorted_months = sorted(files_by_month.keys(), reverse=True)

    with open(output_filename, "w", encoding="utf-8") as outfile:
        outfile.write("# Blog Post Index\n\n") # Updated main heading
        for month_key in sorted_months:
            # Format month for the header
            outfile.write(f"# {month_key}\n\n")
            # Sort files within each month, first by original date, then by title
            sorted_files = sorted(files_by_month[month_key], key=lambda x: (x[0], x[0].lower()))
            for title, permalink, _ in sorted_files:
                # Create a Markdown link to the blog post's permalink
                outfile.write(f"- [{title}]({permalink})\n")
            outfile.write("\n")
        outfile.write("\n ## More from me at: https://about.mvaldes.dev")

    print(f"Generated {output_filename} successfully with custom blog URLs!")

if __name__ == "__main__":
    # --- Configuration ---
    # Specify the directory where your blog post markdown files are located
    input_dir = "/home/mvaldes/git/blog/content/" # e.g., "content/posts" or "my_blog_repo/posts"

    # Define the base URL for your blog posts
    # This is crucial for generating the correct permalinks
    # Example: "https://mycoolblog.com/archive/"
    # Example: "https://yourblog.com/posts/" (if your posts are under a 'posts' path)
    base_blog_url = "https://mvaldes.dev" # <--- **CHANGE THIS TO YOUR BLOG'S BASE URL**

    # The output file will be named 'index.md' in the same directory as the script.
    # For a blog, you might place this in a 'content' or 'archive' folder.
    output_file = "index.md"


    # --- Create some dummy markdown files with frontmatter for testing ---
    if os.path.exists(input_dir):
        # --- Run the grouping script ---
        generate_grouped_blog_index(input_dir, base_blog_url, output_file)
