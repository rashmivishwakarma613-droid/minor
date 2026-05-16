CREATE DATABASE ai_exam_db;
USE ai_exam_db;
SHOW TABLES;
CREATE TABLE questions (
id INT AUTO_INCREMENT PRIMARY KEY,
year INT,
semester INT,
subject VARCHAR(100),
unit INT,
question TEXT
);
SHOW TABLES;
USE ai_exam_db;

CREATE TABLE visitors (
id INT AUTO_INCREMENT PRIMARY KEY,
ip_address VARCHAR(50),
user_agent TEXT,
visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SHOW TABLES;
INSERT INTO questions (year, semester, subject, unit, question)
VALUES 
(2025,6,'Machine Learning',1,'Define Machine Learning? Discuss the scope and limitations of Machine Learning.'),
(2025,6,'Machine Learning',1,'Explain the role of regression, probability and statistics in Machine Learning.'),

(2025,6,'Machine Learning',2,'What are Auto Encoders? Explain the types of Auto Encoders?'),
(2025,6,'Machine Learning',2,'Explain the types of Gradient descent.'),

(2025,6,'Machine Learning',3,'Explain the process of implementing CNN in tensor flow.'),
(2025,6,'Machine Learning',3,'Define Padding. How does padding works in CNN?'),

(2025,6,'Machine Learning',4,'Discuss the structure of Long Short Term Memory.'),
(2025,6,'Machine Learning',4,'What is Model based and model free learning Q-Learning? Explain.'),

(2025,6,'Machine Learning',5,'Discuss the applications of Machine Learning in Speech Processing.'),
(2025,6,'Machine Learning',5,'Write a short note on Tokenization.'),

(2025,6,'Machine Learning',5,'Explain the different Data Visualization methods in detail.'),
(2025,6,'Machine Learning',5,'Discuss the sigmoid action function in detail.'),

(2025,6,'Machine Learning',5,'Explain the working principle of Markov Decision Process in detail.'),
(2025,6,'Machine Learning',5,'What do you mean by dimension reduction? Discuss in detail.'),

(2025,6,'Machine Learning',5,'Natural Language Processing'),
(2025,6,'Machine Learning',5,'Data Preprocessing'),
(2025,6,'Machine Learning',5,'Batch normalization');
SELECT * FROM questions;
USE ai_exam_db;

INSERT INTO questions (year, semester, subject, unit, question) VALUES
(2024,6,'Machine Learning',1,'List the main types of Machine Learning algorithms and provide examples of applications for each type.'),
(2024,6,'Machine Learning',1,'Describe evaluation metrics used for regression models in Machine Learning.'),

(2024,6,'Machine Learning',1,'Explain the importance of data normalization in Machine Learning.'),
(2024,6,'Machine Learning',2,'Discuss the advantages and limitations of Sigmoid and ReLU activation functions.'),

(2024,6,'Machine Learning',2,'Define Gradient Descent in Machine Learning.'),
(2024,6,'Machine Learning',2,'Explain L1 (Lasso) and L2 (Ridge) regularization.'),

(2024,6,'Machine Learning',3,'List and explain types of padding used in CNN.'),
(2024,6,'Machine Learning',3,'Describe types of transfer learning.'),

(2024,6,'Machine Learning',5,'Explain why high dimensional data can be challenging for machine learning algorithms.'),
(2024,6,'Machine Learning',4,'Define Recurrent Neural Networks (RNN). Explain the types and architecture of RNN.'),

(2024,6,'Machine Learning',4,'Describe the significance of n-gram precision and brevity penalty in BLEU score.'),
(2024,6,'Machine Learning',4,'Explain Actor-Critic model.'),

(2024,6,'Machine Learning',5,'Describe the concept of support vectors in SVM.'),
(2024,6,'Machine Learning',5,'Explain machine learning in speech processing.'),

(2024,6,'Machine Learning',1,'Write short note on Convex optimization.'),
(2024,6,'Machine Learning',2,'Write short note on Linearity vs Non-linearity.'),
(2024,6,'Machine Learning',4,'Write short note on Q-learning.'),
(2024,6,'Machine Learning',4,'Write short note on Markov Decision Process.');

USE ai_exam_db;

INSERT INTO questions (year, semester, subject, unit, question) VALUES

(2022,6,'Machine Learning',1,'What are the basic design issues and approaches to machine learning?'),
(2022,6,'Machine Learning',1,'Define statistical theory and how it is performed in machine learning.'),

(2022,6,'Machine Learning',1,'Differentiate between Training data and Testing data.'),
(2022,6,'Machine Learning',2,'What do you mean by Gradient Descent?'),

(2022,6,'Machine Learning',2,'Write the algorithm for back propagation.'),
(2022,6,'Machine Learning',3,'Explain in detail principal component analysis for dimension reduction.'),

(2022,6,'Machine Learning',4,'What is Reinforcement learning? Explain in detailed concepts.'),
(2022,6,'Machine Learning',5,'Explain Locally weighted linear regression.'),

(2022,6,'Machine Learning',5,'What is model selection in Machine Learning?'),
(2022,6,'Machine Learning',4,'Describe the concept of Markov Decision Process (MDP).'),

(2022,6,'Machine Learning',4,'Explain Q learning algorithm assuming deterministic rewards.'),
(2022,6,'Machine Learning',5,'Explain the concept of Bayesian theorem with an example.'),

(2022,6,'Machine Learning',5,'What is Support Vector Machine (SVM)? Discuss in detail.'),
(2022,6,'Machine Learning',5,'Define Bayesian learning and how it impacts in machine learning?'),

(2022,6,'Machine Learning',1,'Write short note on Convex optimization in machine learning.'),
(2022,6,'Machine Learning',2,'Write short note on Multilayer network.'),
(2022,6,'Machine Learning',4,'Write short note on Attention model.'),
(2022,6,'Machine Learning',5,'Write short note on Natural Language Processing.');

INSERT INTO questions (year, semester, subject, unit, question) VALUES


(2025,6,'Computer Network',1,'Discuss the operating principles of OSI reference model with diagram showing headers and trailers added to user data.'),
(2025,6,'Computer Network',1,'Compare connection oriented and connectionless service.'),


(2025,6,'Computer Network',2,'What is the advantage of Go-Back-N protocol? How is parameter S determined? Explain working in case of errors, lost packets or ACKs.'),


(2025,6,'Computer Network',2,'What do you mean by error detection? Write methods. Encode 8-bit data 1010111 using even parity Hamming code.'),
(2025,6,'Computer Network',3,'Discuss strategies used to avoid collisions in CSMA/CA.'),


(2025,6,'Computer Network',3,'What is Pure ALOHA and Slotted ALOHA? Show that efficiency of slotted ALOHA is twice that of pure ALOHA.'),
(2025,6,'Computer Network',3,'Explain CSMA/CD protocol in detail.'),


(2025,6,'Computer Network',5,'A TCP machine is sending window of 65535 bytes over 1Gbps channel with 10ms delay. Find maximum throughput and line efficiency.'),


(2025,6,'Computer Network',5,'Compare TCP header and UDP header. List fields in TCP not present in UDP with reason.'),

(2025,6,'Computer Network',4,'An organization is granted block 211.17.180.0/24. Create 32 subnets. Find subnet mask, number of addresses, first and last address.'),

(2025,6,'Computer Network',5,'Write short note on TCP Header Format.'),
(2025,6,'Computer Network',5,'Write short note on TCP flow control.'),
(2025,6,'Computer Network',4,'Write short note on ICMP.'),
(2025,6,'Computer Network',4,'Write short note on Bellman Ford Algorithm.');

INSERT INTO questions (year, semester, subject, unit, question) VALUES

(2024,6,'Computer Networks',1,'Explain different types of network topologies with advantages and disadvantages.'),
(2024,6,'Computer Networks',1,'Draw and explain seven layers of OSI reference model and name two protocols of each layer.'),

(2024,6,'Computer Networks',2,'Explain Stop and Wait protocol with diagram.'),
(2024,6,'Computer Networks',2,'Explain Go Back N protocol.'),
(2024,6,'Computer Networks',2,'Explain Selective Repeat protocol.'),

(2024,6,'Computer Networks',5,'Compare TCP header and UDP header. List fields present in TCP but not in UDP.'),

(2024,6,'Computer Networks',4,'Explain various classes of IP addresses with network ID, host ID and range.'),
(2024,6,'Computer Networks',1,'Define data rate and bandwidth with suitable example.'),

(2024,6,'Computer Networks',4,'An organization is granted block 211.17.180.0/24. Create 32 subnets and find subnet mask, number of addresses and range.'),

(2024,6,'Computer Networks',5,'A TCP machine sending window of 65535 bytes over 1Gbps link with 10ms delay. Find maximum throughput and line efficiency.'),

(2024,6,'Computer Networks',5,'What are the parameters of Quality of Service offered by transport layer?'),
(2024,6,'Computer Networks',3,'Explain MAC layer protocols Pure ALOHA, Slotted ALOHA and CSMA.'),

(2024,6,'Computer Networks',1,'Write short note on Connection Oriented service.'),
(2024,6,'Computer Networks',2,'Write short note on ARP.'),
(2024,6,'Computer Networks',3,'Write short note on CSMA/CA.'),
(2024,6,'Computer Networks',5,'Write short note on DNS.');

INSERT INTO questions (year, semester, subject, unit, question) VALUES

(2023,6,'Computer Network',1,
' What is a Computer Network? Discuss the importance of computer network. Give its merits and demerits.'),

(2023,6,'Computer Network',1,
' Explain the working principle of ISO-OSI reference model with the functionality of each layer.'),

(2023,6,'Computer Network',2,
' What is the Data Link Layer and what services does it provide?'),

(2023,6,'Computer Network',2,
' What is the mechanism of sliding window flow control? Explain with an example.'),

(2023,6,'Computer Network',3,
' Discuss guided and unguided transmission media with suitable sketch.'),

(2023,6,'Computer Network',2,
' What is a Finite State Machine (FSM) model? How are finite state machines used in the study of network protocols? Explain.'),

('2023','6','Computer Network','3',
' Explain the working principle of Slotted ALOHA with suitable sketch.'),

('2023','6','Computer Network','3',
' A group of stations share a 56 Kbps pure ALOHA channel. Each station outputs a 1000-bit frame on average once every 100 seconds (stations are buffered). What is the maximum value of N?'),

(2023,6,'Computer Network',4,
' Describe the working principle of Least Cost Routing using a suitable example.'),

('2023','6','Computer Network','4',
' Write a brief note on ICMP (Internet Control Message Protocol) using its frame format.'),

(2023,6,'Computer Network',3,
' What are Limited-Contention Protocols? Explain the working principle of Adaptive Tree Walk Protocol with a suitable example.'),

(2023,6,'Computer Network',4,
' Give a comparative study of IPv4 and IPv6.'),

(2023,6,'Computer Network',5,
' What is Electronic Mailing? What are the different ways of sending electronic mail (E-mail)? Discuss in detail.'),

(2023,6,'Computer Network',5,
' Discuss the concept of TCP flow control and TCP congestion control.'),

(2023,6,'Computer Network',1,
' Service Primitives.'),

(2023,6,'Computer Network',3,
' CSMA/CD.'),

(2023,6,'Computer Network',6,
' IEEE Standards 802 series.'),

(2023,6,'Computer Network',4,
' Fragmentation and reassembly.');

INSERT INTO questions (year, semester, subject, unit, question) VALUES

(2022,6,'Computer Network',1,'Q1(a) Explain the OSI model stating its importance in network architectures.'),

(2022,6,'Computer Network',1,
'Q1(b) What is the principal difference between connectionless and connection-oriented communication?'),

(2022,6,'Computer Network',2,
'Q2(a) Explain data link layer addressing with examples.'),

(2022,6,'Computer Network',3,
'Q2(b) A radio station is using a 14.44 kbps channel for message transmission and the sending message packets are 100 bits long. Calculate the maximum throughput for the channel using Slotted ALOHA.'),

(2022,6,'Computer Network',2,
'Q3(a) Describe the Stop-and-Wait flow control technique.'),

(2022,6,'Computer Network',4,
'Q3(b) What is subnet mask? Explain different classes of IP address.'),

(2022,6,'Computer Network',2,
'Q4(a) Describe Go Back N and Selective Repeat protocol.'),

(2022,6,'Computer Network',2,
'Q4(b) What is bit stuffing and byte stuffing? Explain with example.'),

(2022,6,'Computer Network',5,
'Q5(a) Explain the connection establishment and connection release in transport protocols.'),

(2022,6,'Computer Network',5,
'Q5(b) Describe the Frame Relay protocol architecture and explain the functions of each layer.'),

(2022,6,'Computer Network',6,
'Q6(a) Discuss Internet service standards for TCP/IP and the process of standardization for RFCs and TCP/IP.'),

(2022,6,'Computer Network',4,
'Q6(b) Explain Distance Vector routing with example.'),

(2022,6,'Computer Network',4,
'Q7(a) Explain routing and congestion control.'),

(2022,6,'Computer Network',6,
'Q7(b) Differentiate various broadband network local loop technologies stating their properties.'),

(2022,6,'Computer Network',6,
'Q8(i) FDDI'),

(2022,6,'Computer Network',4,
'Q8(ii) ARP'),

(2022,6,'Computer Network',4,
'Q8(iii) ICMP'),

(2022,6,'Computer Network',5,
'Q8(iv) UDP');

SELECT * FROM visitors;
USE ai_exam_db;
CREATE TABLE feedback(
id INT AUTO_INCREMENT PRIMARY KEY,
question TEXT,
message TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE users(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100),
email VARCHAR(100),
password VARCHAR(100),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
