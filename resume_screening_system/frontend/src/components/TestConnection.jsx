import { useEffect, useState } from 'react';

const API_BASE = '/api';

export default function TestConnection() {
  const [status, setStatus] = useState('Testing...');
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/`)
      .then(res => res.json())
      .then(data => {
        setStatus('✅ Connected!');
        setResult(data);
      })
      .catch(err => {
        setStatus('❌ Failed: ' + err.message);
      });
  }, []);

  const uploadTest = async () => {
    const formData = new FormData();
    formData.append('test', 'Hello Backend');
    
    try {\n      const res = await fetch(`${API_BASE}/v1/`, {\n        method: 'POST',\n        body: formData\n      });
      const data = await res.json();
      console.log('Upload success:', data);
    } catch (err) {
      console.error('Upload error:', err);
    }
  };

  return (
    <div className="p-4 border">
      <h2>Backend Connection Test</h2>
      <p>Status: {status}</p>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
      <button onClick={uploadTest} className="mt-2 p-2 bg-blue-500 text-white">Test Upload</button>
    </div>
  );
}
