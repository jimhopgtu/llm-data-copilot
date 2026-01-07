'use client';

import { useState } from 'react';

export default function FileUpload() {
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
  
    setUploading(true);
    setMessage('');
  
    try {
      const formData = new FormData();
      formData.append('file', file);
  
      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });
  
      const data = await response.json();
      
      console.log('Upload response:', data); // Debug log
      
      if (data.success) {
        setMessage(`✅ ${file.name} uploaded successfully!`);
      } else {
        setMessage(`❌ Error: ${data.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Upload error:', error); // Debug log
      setMessage(`❌ Upload failed: ${String(error)}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="mb-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Upload Document
      </label>
      <input
        type="file"
        onChange={handleFileUpload}
        disabled={uploading}
        accept=".txt,.csv,.md"
        className="block w-full text-sm text-gray-500
          file:mr-4 file:py-2 file:px-4
          file:rounded-lg file:border-0
          file:text-sm file:font-semibold
          file:bg-blue-600 file:text-white
          hover:file:bg-blue-700
          file:cursor-pointer
          disabled:opacity-50"
      />
      {uploading && <p className="mt-2 text-sm text-blue-600">Uploading...</p>}
      {message && <p className="mt-2 text-sm">{message}</p>}
    </div>
  );
}