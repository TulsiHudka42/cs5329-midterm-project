
import argparse
import csv
import os
import random

POPULAR_TITLES = [
    "Shape of You", "Believer", "Levitating", "Blinding Lights", "Bad Guy",
    "Someone Like You", "Perfect", "Hello", "Stay", "Senorita"
]
ARTISTS = [
    "Ed Sheeran", "Imagine Dragons", "Dua Lipa", "The Weeknd", "Billie Eilish",
    "Adele", "Justin Bieber", "Taylor Swift", "Drake", "Rihanna"
]
ALBUMS = [
    "Divide", "Evolve", "Future Nostalgia", "After Hours", "When We All Fall Asleep",
    "25", "Justice", "Midnights", "Scorpion", "Anti"
]


def generate_dataset(size: int, output_path: str) -> None:
    random.seed(5329 + size)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["track_name", "artist_name", "album_name", "duration_ms", "popularity"],
        )
        writer.writeheader()

        for i in range(size):
            if i < len(POPULAR_TITLES) * 50:
                title = POPULAR_TITLES[i % len(POPULAR_TITLES)]
            else:
                title = f"Song_{i:07d}"

            writer.writerow(
                {
                    "track_name": title,
                    "artist_name": random.choice(ARTISTS),
                    "album_name": random.choice(ALBUMS),
                    "duration_ms": random.randint(120000, 320000),
                    "popularity": random.randint(1, 100),
                }
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int, default=[10000, 50000, 100000])
    parser.add_argument("--output_dir", default="data")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    for size in args.sizes:
        path = os.path.join(args.output_dir, f"songs_{size}.csv")
        generate_dataset(size, path)
        print(f"Created {path}")


if __name__ == "__main__":
    main()
