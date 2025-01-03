import React, { useState, useRef, useEffect } from 'react';

const Assistant: React.FC = () => {
    const [recording, setRecording] = useState(false);
    const [processingMessage, setProcessingMessage] = useState(false);
    const [audioURL, setAudioURL] = useState<string | null>(null);
    const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
    const [textMessages, setTextMessages] = useState<{
        text: string;
        user: boolean;
    }[]>([]);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const audioChunksRef = useRef<Blob[]>([]);
    const baseUrl = 'http://localhost:8000';

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
        setRecording(false);
        if (!mediaRecorderRef.current) {
            return;
        }

        mediaRecorderRef.current.onstop = () => {
            const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
            const audioURL = URL.createObjectURL(audioBlob);
            setAudioURL(audioURL);
            setAudioBlob(audioBlob);
            audioChunksRef.current = [];

            handleUpload();
        };

        mediaRecorderRef.current.stop();
    };

    const handleAskQuestion = async (question: string) => {
        const formData = new FormData();
        formData.append('question', question);

        const response: {
            response: string;
        } = await fetch(`${baseUrl}/ask_question`, {
            method: 'POST',
            body: formData,
        }).then((response) => response.json());

        setTextMessages((prev) => [...prev, { text: response.response, user: false }]);
        setProcessingMessage(false);
    };


    useEffect(() => {
        if (!audioBlob) {
            return;
        }
        async function handleUpload() {
            setProcessingMessage(true);

            const formData = new FormData();
            formData.append('audio_file', audioBlob!, 'recording.wav');

            const response: {
                transcription: string;
            } = await fetch(`${baseUrl}/transcribe_audio`, {
                method: 'POST',
                body: formData,
            }).then((response) => response.json());

            setTextMessages((prev) => [...prev, { text: response.transcription, user: true }]);

            handleAskQuestion(response.transcription);
        }
        handleUpload();
    }, [ audioBlob ]);

    return (
        <div>   
            <div
                onMouseDown={handleMouseDown}
                onMouseUp={handleMouseUp}
            >
                <button disabled={processingMessage}>
                    {
                    recording ?
                        'Grabando...' :
                        processingMessage ? 'Procesando...' :
                            'Presiona para hablar'
                    }
                </button>
            </div>
            {audioURL && (
                <div>
                    <audio controls src={audioURL} />
                </div>
            )}
            <div className='chat-box'>
                {textMessages.map((message, index) => (
                    <div className={['chat-bubble', message.user ? 'own' : ''].join(" ")} key={index}>
                        <span>{message.user ? 'Usuario: ' : 'Asistente: '}</span>
                        <span>{message.text}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Assistant;
