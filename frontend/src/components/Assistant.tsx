import React, { useState, useRef } from 'react';

const Assistant: React.FC = () => {
    const [recording, setRecording] = useState(false);
    const [audioURL, setAudioURL] = useState<string | null>(null);
    const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const audioChunksRef = useRef<Blob[]>([]);
    const baseUrl = 'http://localhost:8000/transcribe_audio';

    const handleMouseDown = async (e: React.MouseEvent<HTMLDivElement>) => {
        console.log('Mouse down', e);

        setRecording(true);
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorderRef.current = mediaRecorder;

        mediaRecorder.ondataavailable = (event) => {
            audioChunksRef.current.push(event.data);
        };

        mediaRecorder.start();
    };

    const handleMouseUp = (e: React.MouseEvent<HTMLDivElement>) => {
        console.log('Mouse up', e);

        setRecording(false);
        if (mediaRecorderRef.current) {
            mediaRecorderRef.current.stop();
            mediaRecorderRef.current.onstop = () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
                const audioURL = URL.createObjectURL(audioBlob);
                setAudioURL(audioURL);
                setAudioBlob(audioBlob);
                audioChunksRef.current = [];
            };
        }
    };

    const handleUpload = async () => {
        if (audioBlob) {
            const formData = new FormData();
            formData.append('audio_file', audioBlob, 'recording.wav');

            await fetch(baseUrl, {
                method: 'POST',
                body: formData,
            });

            alert('Audio file uploaded successfully!');
        }
    };

    return (
        <div
            onMouseDown={handleMouseDown}
            onMouseUp={handleMouseUp}
        >
            <button>
                {recording ? 'Recording...' : 'Hold to Record'}
            </button>
            {audioURL && (
                <div>
                    <audio controls src={audioURL} />
                    <button onClick={handleUpload}>Upload Audio</button>
                </div>
            )}
        </div>
    );
};

export default Assistant;
