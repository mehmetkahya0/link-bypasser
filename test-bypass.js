// Quick test for the specific is.gd link
// You can run this in the browser console to test the bypass

async function testIsGdBypass() {
    const url = 'https://is.gd/exTZy1';
    
    console.log('Testing is.gd bypass for:', url);
    
    // Method 1: Try preview page
    try {
        const previewUrl = url + '-';
        console.log('Trying preview method with:', previewUrl);
        
        const response = await fetch(`https://api.allorigins.win/get?url=${encodeURIComponent(previewUrl)}`);
        const data = await response.json();
        console.log('Preview response:', data);
        
        const html = data.contents;
        
        // Look for the destination URL
        const match = html.match(/<p[^>]*>Destination URL:[^<]*<a[^>]+href\s*=\s*["']([^"']+)["']/i);
        if (match) {
            console.log('Found destination URL:', match[1]);
            return match[1];
        }
        
        // Alternative pattern
        const match2 = html.match(/href\s*=\s*["']([^"']+)["'][^>]*>[\s]*https?:\/\//i);
        if (match2) {
            console.log('Found alternative URL:', match2[1]);
            return match2[1];
        }
        
        console.log('No URL found in preview page');
        console.log('HTML snippet:', html.substring(0, 500));
        
    } catch (error) {
        console.error('Preview method failed:', error);
    }
    
    // Method 2: Try direct resolution
    try {
        console.log('Trying direct resolution...');
        const response = await fetch(`https://corsproxy.io/?${encodeURIComponent(url)}`, {
            method: 'HEAD',
            redirect: 'manual'
        });
        
        const location = response.headers.get('location');
        if (location) {
            console.log('Found redirect location:', location);
            return location;
        }
        
    } catch (error) {
        console.error('Direct resolution failed:', error);
    }
    
    console.log('All methods failed');
    return null;
}

// Run the test
testIsGdBypass().then(result => {
    console.log('Final result:', result);
}).catch(error => {
    console.error('Test failed:', error);
});
