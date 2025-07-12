// Google Drive upload using Google Identity Services (GIS)
// Make sure to add this to your public/index.html:
// <script src="https://accounts.google.com/gsi/client" async defer></script>

// IMPORTANT: Set your Google OAuth Client ID in your .env file as VITE_GOOGLE_CLIENT_ID
const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
const FOLDER_ID = '1xj8c1YfG0PtrK5TonpRppYKe55PLWHpP';
const SCOPES = 'https://www.googleapis.com/auth/drive.file';

let tokenClient: any;

// Add this at the top of the file for TypeScript compatibility
// @ts-ignore
declare global {
  interface Window {
    google?: any;
  }
}

export function initGoogleIdentity() {
  if (!window.google || !window.google.accounts) {
    console.error('Google Identity Services not loaded. Make sure the GIS script is included in index.html.');
    return;
  }
  tokenClient = window.google.accounts.oauth2.initTokenClient({
    client_id: CLIENT_ID,
    scope: SCOPES,
    callback: () => {}, // will be set per request
  });
}

export function requestAccessToken(callback: (accessToken: string) => void) {
  if (!tokenClient) {
    initGoogleIdentity();
  }
  if (!tokenClient) {
    throw new Error('Google Identity client not initialized. Make sure initGoogleIdentity() is called and GIS script is loaded.');
  }
  tokenClient.callback = (tokenResponse: any) => {
    callback(tokenResponse.access_token);
  };
  tokenClient.requestAccessToken();
}

export function uploadPdfToDriveWithGIS(file: Blob, fileName: string): Promise<string> {
  return new Promise((resolve, reject) => {
    requestAccessToken(async (accessToken) => {
      try {
        const metadata = {
          name: fileName,
          mimeType: 'application/pdf',
          parents: [FOLDER_ID],
        };
        const form = new FormData();
        form.append('metadata', new Blob([JSON.stringify(metadata)], { type: 'application/json' }));
        form.append('file', file);
        const response = await fetch(
          'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id',
          {
            method: 'POST',
            headers: new Headers({ Authorization: 'Bearer ' + accessToken }),
            body: form,
          }
        );
        const data = await response.json();
        const fileId = data.id;
        // Make the file public
        await fetch(
          `https://www.googleapis.com/drive/v3/files/${fileId}/permissions`,
          {
            method: 'POST',
            headers: {
              Authorization: 'Bearer ' + accessToken,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              role: 'reader',
              type: 'anyone',
            }),
          }
        );
        // Return the shareable link
        resolve(`https://drive.google.com/file/d/${fileId}/view?usp=sharing`);
      } catch (err) {
        reject(err);
      }
    });
  });
} 