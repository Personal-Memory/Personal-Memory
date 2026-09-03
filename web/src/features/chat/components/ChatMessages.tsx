import MessageBubble from "./MessageBubble";

const messages = [
    {
        role: "user" as const,
        content: "What did I learn about machine learning yesterday?",
    },

    {
        role: "assistant" as const,
        content: "Yesterday, you learned about the basics of machine learning, including supervised and unsupervised learning, as well as some common algorithms like linear regression and decision trees.",
    },

    {
        role: "user" as const,
        content: "Can you give me a brief summary of the key concepts?",
    },

    {
        role: "assistant" as const,
        content: "Sure! The key concepts of machine learning include:\n\n1. Supervised Learning: A type of machine learning where the model is trained on labeled data, meaning that the input data is paired with the correct output. The goal is to learn a mapping from inputs to outputs.\n\n2. Unsupervised Learning: A type of machine learning where the model is trained on unlabeled data, meaning that the input data does not have corresponding output labels. The goal is to find patterns or structure in the data.\n\n3. Common Algorithms: Some common algorithms used in machine learning include linear regression, decision trees, k-nearest neighbors, and support vector machines.\n\n4. Model Evaluation: After training a model, it is important to evaluate its performance using metrics such as accuracy, precision, recall, and F1 score.\n\n5. Overfitting and Underfitting: Overfitting occurs when a model learns the training data too well"
    },
];

function ChatMessages() {
    return (
        <div className="flex-1 overflow-y-auto px-6 py-8">
            <div className="mx-auto max-w-3xl space-y-6">
                {messages.map((message, index) => (
                    <MessageBubble
                        key={index}
                        role={message.role}
                        content={message.content}
                    />
                ))}
            </div>
        </div>
    );
}

export default ChatMessages;