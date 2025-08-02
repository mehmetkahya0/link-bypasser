#!/usr/bin/env python3
"""
Link Generator Script for LinkBypass Pro
Generates real working shortened links for testing purposes
"""

import requests
import json
import time
from urllib.parse import quote

class LinkGenerator:
    def __init__(self):
        self.generated_links = []
        self.popular_urls = [
            "https://www.google.com",
            "https://www.youtube.com",
            "https://www.github.com",
            "https://www.stackoverflow.com",
            "https://www.wikipedia.org",
            "https://www.reddit.com",
            "https://www.twitter.com",
            "https://www.facebook.com",
            "https://www.instagram.com",
            "https://www.linkedin.com",
            "https://www.amazon.com",
            "https://www.netflix.com",
            "https://www.spotify.com",
            "https://www.apple.com",
            "https://www.microsoft.com",
            "https://www.discord.com",
            "https://www.twitch.tv",
            "https://www.tiktok.com",
            "https://www.pinterest.com",
            "https://www.dropbox.com"
        ]

    def generate_tinyurl(self, long_url):
        """Generate a TinyURL shortened link"""
        try:
            api_url = f"https://tinyurl.com/api-create.php?url={quote(long_url)}"
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200 and response.text.startswith('https://tinyurl.com/'):
                return response.text.strip()
        except Exception as e:
            print(f"TinyURL error: {e}")
        return None

    def generate_is_gd(self, long_url):
        """Generate an is.gd shortened link"""
        try:
            api_url = f"https://is.gd/create.php?format=simple&url={quote(long_url)}"
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200 and response.text.startswith('https://is.gd/'):
                return response.text.strip()
        except Exception as e:
            print(f"is.gd error: {e}")
        return None

    def generate_v_gd(self, long_url):
        """Generate a v.gd shortened link"""
        try:
            api_url = f"https://v.gd/create.php?format=simple&url={quote(long_url)}"
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200 and response.text.startswith('https://v.gd/'):
                return response.text.strip()
        except Exception as e:
            print(f"v.gd error: {e}")
        return None

    def generate_cutt_ly(self, long_url, api_key=None):
        """Generate a cutt.ly shortened link (requires API key)"""
        if not api_key:
            print("Cutt.ly requires an API key. Skipping...")
            return None
        
        try:
            api_url = "https://cutt.ly/api/api.php"
            data = {
                'key': api_key,
                'short': long_url
            }
            response = requests.post(api_url, data=data, timeout=10)
            result = response.json()
            if result.get('url', {}).get('status') == 7:
                return result['url']['shortLink']
        except Exception as e:
            print(f"Cutt.ly error: {e}")
        return None

    def generate_batch_links(self, count=100):
        """Generate a batch of shortened links"""
        print(f"Generating {count} shortened links...")
        
        services = [
            ("TinyURL", self.generate_tinyurl),
            ("is.gd", self.generate_is_gd),
            ("v.gd", self.generate_v_gd),
        ]
        
        generated_count = 0
        
        for i, url in enumerate(self.popular_urls * 5):  # Repeat URLs to get more links
            if generated_count >= count:
                break
                
            for service_name, generator_func in services:
                if generated_count >= count:
                    break
                    
                print(f"Generating {service_name} link {generated_count + 1}/{count}...")
                
                try:
                    short_link = generator_func(url)
                    if short_link:
                        self.generated_links.append({
                            'service': service_name,
                            'short_url': short_link,
                            'original_url': url,
                            'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
                        })
                        generated_count += 1
                        print(f"✓ Generated: {short_link}")
                    else:
                        print(f"✗ Failed to generate {service_name} link")
                        
                    # Rate limiting
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"✗ Error with {service_name}: {e}")
                    continue
        
        return self.generated_links

    def save_to_file(self, filename="generated_links.txt"):
        """Save generated links to a text file"""
        with open(filename, 'w') as f:
            f.write("# Generated Working Shortened Links\n")
            f.write(f"# Created on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Total links: {len(self.generated_links)}\n\n")
            
            # Group by service
            services = {}
            for link in self.generated_links:
                service = link['service']
                if service not in services:
                    services[service] = []
                services[service].append(link)
            
            for service, links in services.items():
                f.write(f"# {service} Links ({len(links)} total)\n")
                for link in links:
                    f.write(f"{link['short_url']}\n")
                f.write("\n")
        
        print(f"✓ Saved {len(self.generated_links)} links to {filename}")

    def save_to_json(self, filename="generated_links.json"):
        """Save generated links to a JSON file with metadata"""
        with open(filename, 'w') as f:
            json.dump({
                'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_count': len(self.generated_links),
                'links': self.generated_links
            }, f, indent=2)
        
        print(f"✓ Saved detailed data to {filename}")

def main():
    print("LinkBypass Pro - Link Generator")
    print("=" * 40)
    
    generator = LinkGenerator()
    
    # Generate links
    links = generator.generate_batch_links(50)  # Generate 50 links (adjust as needed)
    
    if links:
        # Save to files
        generator.save_to_file("working_shortened_links.txt")
        generator.save_to_json("link_data.json")
        
        print(f"\n✓ Successfully generated {len(links)} working shortened links!")
        print("Files created:")
        print("- working_shortened_links.txt (for testing)")
        print("- link_data.json (detailed data)")
    else:
        print("✗ No links were generated. Check your internet connection.")

if __name__ == "__main__":
    main()
