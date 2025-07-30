import { useState } from 'react'

const ChatBot = () => {
  const [query, setQuery] = useState("")
  const [answer, setAnswer] = useState("")
  const [loading, setLoading] = useState(false)

  const handleAsk = async () => {
    setLoading(true)
    try {
      const res = await fetch("https://portfolio-react-with-rag-chatbot.onrender.com", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }) // payload
      })
      const data = await res.json()
      setAnswer(data.answer)
    } catch (err) {
      console.error("Error:", err)
      setAnswer("Something went wrong")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Ask the Chatbot</h2>
      <textarea
        className="w-full p-2 border rounded text-white bg-gray-950"
        rows="4"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Type your question..."
      />
      <button
        onClick={handleAsk}
        className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
      >
        {loading ? 'Thinking...' : 'Ask'}
      </button>

      <div className="flex gap-2 mt-2">
        <button
          onClick={() => setQuery("")}
          className="px-4 py-2 bg-gray-600 text-white rounded"
        >
          Clear
        </button>
        <button
          onClick={() => {
            setQuery("")
            setAnswer("")
          }}
          className="px-4 py-2 bg-red-500 text-white rounded"
        >
          End Chat
        </button>
      </div>

      {answer && (
        <div className="mt-4 p-4 border rounded bg-gray-900 text-white">
          <strong>Answer:</strong> {answer}
        </div>
      )}
    </div>
  )
}

export default ChatBot
