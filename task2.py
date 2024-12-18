import signal
import sys
import requests
import re
import string
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import logging
import argparse

logger = logging.getLogger(__name__)
# Global flag to track if the program has already received Ctrl+C
interrupted = False


def handle_sigint(signum, frame):
    global interrupted
    if not interrupted:
        interrupted = True
        logger.info("Operation cancelled (Ctrl+C). Exiting the application.")
    sys.exit(0)


# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, handle_sigint)


def fetch_text_from_url(url) -> str:
    """
    Downloads text from the specified URL.
    Args:
        url (str): URL address to download text from.
    Returns:
        str: Text downloaded from the URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except (
        requests.exceptions.RequestException,
        requests.exceptions.HTTPError,
    ) as e:
        logger.error(f"Error fetching data from {url}: {e}")
        return ""


def tokenize(text) -> list:
    """
    Converts text into a list of words.
    Args:
        text (str): Text to tokenize.
        Returns:
            list: List of words.
    """
    try:
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        words = re.findall(r"\w+", text)
        return words
    except Exception as e:
        logger.error(f"Error during tokenization: {e}")
        return []


def mapper(chunk) -> list:
    """
    Map function: transforms a list of words into a list of pairs (word, 1).
    Args:
        chunk (list): List of words.
    Returns:
        list: List of pairs (word, 1).
    """
    return [(word, 1) for word in chunk]


def shuffle_function(mapped_results) -> dict:
    """
    Shuffle function: groups results by keys (words).
    Args:
        mapped_results (list): List of results from map,
            each of which is a list of pairs (word, 1).
    Returns:
        dict: Dictionary {word: total_count}
    """
    shuffled = defaultdict(int)
    try:
        for part in mapped_results:
            for word, count in part:
                # Sum up the counts for each word insted of storing a list of
                # counts for each word is a better approach in my opinion
                # since it reduces the memory usage and makes the reduce phase
                shuffled[word] += count
        return shuffled
    except Exception as e:
        logger.error(f"Error during shuffling: {e}")
        return {}


def reducer(shuffled_data) -> dict:
    """
    Reduce function.
    Args:
        shuffled_data (dict): Dictionary {word: total_count}
    Returns:
        dict: Final reduced result containing word counts
    """
    try:
        return Counter(shuffled_data)
    except Exception as e:
        logger.error(f"Error during reduction: {e}")
        return Counter()


def parallel_map_reduce(words, num_workers=4) -> dict:
    """
    Performs MapReduce in multi-threaded mode with separate shuffle phase.
    Args:
        words (list): Input list of words to process
        num_workers (int): Number of worker threads to use. Defaults to 4.
    Returns:
        dict: Final reduced result containing word counts
    """
    try:
        if not words:
            raise ValueError("No words provided for MapReduce.")
        words_len = len(words)
        chunk_size = (
            words_len // num_workers if words_len > num_workers else words_len
        )
        chunks = [
            words[i: i + chunk_size] for i in range(0, words_len, chunk_size)
        ]

        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            # Map phase
            map_results = list(executor.map(mapper, chunks))

        # In this case, we can use a single thread for the shuffle and reduce
        # phases since the data is already split into chunks and the shuffle
        # phase is not computationally intensive
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            # Shuffle phase
            shuffled = shuffle_function(map_results)

            # Reduce phase
            final_result = list(executor.map(reducer, [shuffled]))[0]

        return final_result
    except Exception as e:
        logger.error(f"Error during MapReduce: {e}")
        return {}


def visualize_top_words(word_counts, top_n=10) -> None:
    """
    Visualizes the top N most common words.
    Args:
        word_counts (dict): Dictionary containing word counts
        top_n (int): Number of top words to visualize. Defaults to 10.
    Returns:
        None
    """
    try:
        top_words = word_counts.most_common(top_n)
        if not top_words:
            logger.info("No words to display.")
            return
        words, freqs = zip(*top_words)

        plt.figure(figsize=(10, 6))
        plt.barh(words[::-1], freqs[::-1], color="skyblue")
        plt.title(f"Top {top_n} Most Common Words")
        plt.xlabel("Frequency")
        plt.ylabel("Words")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        logger.error(f"Error during visualization: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MapReduce Word Count")
    parser.add_argument(
        "--url",
        type=str,
        default="https://www.gutenberg.org/files/98/98-0.txt",
        help="URL to fetch text from",
    )
    parser.add_argument(
        "--num_workers", type=int, default=4, help="Number of worker threads"
    )
    parser.add_argument(
        "--top_n", type=int, default=10, help="Number of top words to display"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logger level (default: INFO).",
    )
    parser.add_argument(
        "--path-to-log",
        default="task2.log",
        help="Path to the log file (default: application.log).",
    )
    args = parser.parse_args()

    # Set logger level based on argument
    logging.basicConfig(
        level=args.log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(args.path_to_log, mode="a", encoding="utf-8"),
        ],
    )

    try:
        logger.info(f"Fetching text from {args.url}")
        text = fetch_text_from_url(args.url)
        if not text:
            raise ValueError("Failed to fetch text from the URL.")

        logger.info("Tokenizing text")
        words = tokenize(text)
        if not words:
            raise ValueError("No words were extracted from the text.")

        logger.info("Performing MapReduce")
        word_frequencies = parallel_map_reduce(
            words, num_workers=args.num_workers
        )
        if not word_frequencies:
            raise ValueError("Failed to compute word frequencies.")

        logger.info(f"Visualizing top {args.top_n} words")
        visualize_top_words(word_frequencies, top_n=args.top_n)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
