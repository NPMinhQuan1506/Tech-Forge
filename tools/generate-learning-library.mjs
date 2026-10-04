import { mkdirSync, writeFileSync, rmSync } from "node:fs";
import { join } from "node:path";

const outDir = join(process.cwd(), "featlearn_ts_scss", "learning-library");
const chapterDir = join(outDir, "chapters");
const assetDir = join(outDir, "assets");

const standardLens = [
  "Concept",
  "Problem it solves",
  "Primitive model",
  "Under the hood",
  "Practice",
  "Debug / observe",
  "Trade-offs",
  "AI-aware engineering",
];

const parts = [
  {
    id: "intro",
    title: "Introduction",
    chapters: [
      {
        n: "00",
        title: "Introduction",
        summary:
          "Welcome, learning philosophy, topic template, and the operating principles of the library.",
        sections: [
          ["00.1", "Welcome", ["What this library is", "Who it is for", "How it differs from tutorial sites", "How to read this book"]],
          ["00.2", "The Zen Of This Book", ["Micro practice, macro vision", "Primitive before abstraction", "Problem before technology", "Observation before guessing", "AI as leverage"]],
          ["00.3", "How To Learn From This Book", ["Read the concept", "Build the primitive", "Observe the runtime", "Break intentionally", "Explain it back"]],
          ["00.4", "Topic Template", ["What", "Why", "Problem before it", "Internals", "Failure modes", "Trade-offs", "Exercises", "Vocabulary"]],
        ],
      },
    ],
  },
  {
    id: "part-i",
    title: "Part I. Computer From The Bottom Up",
    chapters: [
      {
        n: "01",
        title: "Information, Bits, And Representation",
        summary:
          "How physical signals become bits, bytes, numbers, text, files, and media.",
        sections: [
          ["01.1", "Why Computers Need Representation", ["Physical reality to symbol", "Signal to bit", "Bit to meaning", "Same bits, different meanings"]],
          ["01.2", "Binary", ["Decimal vs binary", "Base-2 place value", "Counting in binary", "Binary addition", "Overflow", "Binary in code", "Build a converter"]],
          ["01.3", "Bits And Bytes", ["Bit", "Nibble", "Byte", "Word", "16/32/64-bit", "KB vs KiB", "Inspect bytes in a file"]],
          ["01.4", "Boolean Logic", ["True and false", "NOT", "AND", "OR", "XOR", "Truth tables", "Logic gates", "Build gates in code"]],
          ["01.5", "Number Representation", ["Unsigned integer", "Signed integer", "Sign bit", "One's complement", "Two's complement", "Sign extension", "Floating point", "IEEE 754"]],
          ["01.6", "Text Representation", ["Character", "ASCII", "Code page", "Unicode", "UTF-8", "UTF-16", "Emoji as data", "Encoding bugs"]],
          ["01.7", "Data Representation In Practice", ["Image bytes", "Audio samples", "Video frames", "File format", "Header", "Metadata", "Compression", "Read a file header"]],
        ],
      },
      {
        n: "02",
        title: "From Logic To Hardware",
        summary:
          "The path from boolean logic to circuits, registers, memory cells, and a tiny ALU.",
        sections: [
          ["02.1", "Digital Circuits", ["Circuit", "Gate", "Wire", "Signal", "Clock", "Combinational logic", "Sequential logic"]],
          ["02.2", "Building Blocks", ["Half adder", "Full adder", "Multiplexer", "Decoder", "Flip-flop", "Register", "Counter", "Tiny ALU simulation"]],
          ["02.3", "Memory Cells", ["Bit storage", "SRAM", "DRAM", "Address line", "Data line", "Read operation", "Write operation"]],
        ],
      },
      {
        n: "03",
        title: "Computer Architecture",
        summary:
          "CPU, instruction cycle, memory hierarchy, cache, buses, interrupts, and parallel hardware.",
        sections: [
          ["03.1", "CPU Mental Model", ["Instruction", "Register", "ALU", "Control unit", "Program counter", "Stack pointer", "Status flags"]],
          ["03.2", "Instruction Cycle", ["Fetch", "Decode", "Execute", "Memory access", "Write back", "Branching", "Toy CPU emulator"]],
          ["03.3", "CPU Performance", ["Clock cycle", "CPI", "Pipeline", "Pipeline hazard", "Branch prediction", "Out-of-order execution", "Cache miss"]],
          ["03.4", "Memory Hierarchy", ["Register", "L1 cache", "L2 cache", "L3 cache", "RAM", "SSD", "Disk", "Locality", "Cache line", "Measure cache effects"]],
          ["03.5", "Buses And Interrupts", ["Peripheral bus", "I/O space", "Interrupt", "Trap", "Exception", "DMA", "USB", "Saving state"]],
          ["03.6", "Parallel Hardware", ["Multi-core", "Hyperthreading", "SIMD", "GPU", "NUMA", "Cache coherency", "Memory ordering", "Atomic operation"]],
        ],
      },
      {
        n: "04",
        title: "Operating Systems",
        summary:
          "Operating systems as abstraction layer, resource manager, security boundary, and standard interface.",
        sections: [
          ["04.1", "Why Operating Systems Exist", ["Hardware is hard to use directly", "OS as abstraction layer", "OS as resource manager", "OS as security boundary", "OS as standard interface"]],
          ["04.2", "Kernel And User Space", ["Kernel", "User space", "Privilege level", "Ring model", "Trap", "Interrupt", "Exception", "System call"]],
          ["04.3", "System Calls", ["open", "read", "write", "close", "fork", "exec", "wait", "mmap", "Trace a system call"]],
          ["04.4", "Files And File Descriptors", ["Everything is a file", "File descriptor", "stdin", "stdout", "stderr", "Redirection", "Pipe", "Socket as file", "Implement a pipe demo"]],
          ["04.5", "File Systems", ["File", "Directory", "Path", "Permission", "Mount", "Inode", "Buffering", "Journaling"]],
        ],
      },
      {
        n: "05",
        title: "Process, Threads, And Memory",
        summary:
          "Process state, threads, stack, heap, virtual memory, page tables, TLB, and page cache.",
        sections: [
          ["05.1", "Process", ["Process ID", "Parent process", "Child process", "Process state", "Process table", "Zombie process", "Context switch"]],
          ["05.2", "Program Memory Layout", ["Text segment", "Data segment", "BSS", "Heap", "Stack", "Environment", "Arguments", "Print memory addresses"]],
          ["05.3", "Threads", ["Thread vs process", "Shared address space", "Thread stack", "Race condition", "Mutex", "Semaphore", "Deadlock", "Thread pool"]],
          ["05.4", "Virtual Memory", ["Virtual address", "Physical address", "Page", "Frame", "Page table", "TLB", "Page fault", "Copy-on-write", "mmap", "Swap", "Page cache"]],
        ],
      },
      {
        n: "06",
        title: "Toolchain And Executables",
        summary:
          "From source code to executable: preprocessing, compilation, assembly, linking, loading, ELF/PE/Mach-O, and dynamic linking.",
        sections: [
          ["06.1", "From Source Code To Program", ["Source file", "Preprocessing", "Compilation", "Assembly", "Linking", "Executable", "Loading", "Running"]],
          ["06.2", "Compiler", ["Lexing", "Parsing", "AST", "Type checking", "IR", "Optimization", "Code generation"]],
          ["06.3", "Assembler And Linker", ["Object file", "Symbol", "Relocation", "Static linking", "Dynamic linking", "Shared library", "Symbol resolution"]],
          ["06.4", "Executable Format", ["Binary format", "ELF", "PE", "Mach-O", "Header", "Section", "Segment", "Entry point", "Inspect an executable"]],
          ["06.5", "Dynamic Linking", ["Dynamic linker", "GOT", "PLT", "Position independent code", "Library version", "Symbol binding", "ldd / loader diagnostics"]],
        ],
      },
    ],
  },
  {
    id: "part-ii",
    title: "Part II. Programming And Algorithms",
    chapters: [
      {
        n: "07",
        title: "Programming Fundamentals",
        summary:
          "Execution, values, types, control flow, functions, scope, errors, and modules.",
        sections: [
          ["07.1", "Program Execution", ["Source code", "Statement", "Expression", "Runtime", "Input", "Output", "Error", "Exit code"]],
          ["07.2", "Values And Types", ["Value", "Variable", "Constant", "Primitive type", "Composite type", "Value type", "Reference type", "Type conversion", "Type safety"]],
          ["07.3", "Control Flow", ["If", "Else", "Switch", "Loop", "Break", "Continue", "Return", "Recursion"]],
          ["07.4", "Functions", ["Function", "Parameter", "Argument", "Return value", "Scope", "Closure", "Pure function", "Side effect"]],
          ["07.5", "Error Handling", ["Error", "Exception", "Result type", "Validation error", "Runtime error", "Fail fast", "Graceful recovery"]],
        ],
      },
      {
        n: "08",
        title: "Programming Paradigms",
        summary:
          "Procedural, object-oriented, functional, event-driven, concurrent, and reactive programming.",
        sections: [
          ["08.1", "Procedural Programming", ["Procedure", "Step-by-step execution", "Shared state", "Procedural design trade-offs"]],
          ["08.2", "Object-Oriented Programming", ["Object", "Class", "Encapsulation", "Inheritance", "Polymorphism", "Composition", "Interface", "OOP trade-offs"]],
          ["08.3", "Functional Programming", ["Function as value", "Immutability", "Pure function", "Higher-order function", "Map", "Filter", "Reduce", "Functional trade-offs"]],
          ["08.4", "Event-Driven Programming", ["Event", "Listener", "Callback", "Event loop", "Pub/sub", "Event-driven trade-offs"]],
          ["08.5", "Concurrent Programming", ["Task", "Thread", "Coroutine", "Async", "Lock", "Race condition", "Deadlock"]],
          ["08.6", "Reactive Programming", ["Stream", "Observable", "Backpressure", "Subscription", "Reactive UI", "Reactive trade-offs"]],
        ],
      },
      {
        n: "09",
        title: "Data Structures",
        summary:
          "Structures that organize data for access, search, insertion, deletion, traversal, and locality.",
        sections: [
          ["09.1", "Data Structure Foundations", ["Access", "Search", "Insert", "Delete", "Traverse", "Memory layout"]],
          ["09.2", "Linear Structures", ["Array", "Dynamic array", "Linked list", "Stack", "Queue", "Deque"]],
          ["09.3", "Hash-Based Structures", ["Hash function", "Hash table", "Collision", "Chaining", "Open addressing", "Hash set", "Hash map"]],
          ["09.4", "Tree Structures", ["Tree", "Binary tree", "BST", "Balanced tree", "Heap", "Trie", "B-tree"]],
          ["09.5", "Graphs", ["Node", "Edge", "Directed graph", "Undirected graph", "Weighted graph", "Adjacency list", "Adjacency matrix"]],
          ["09.6", "Probabilistic Structures", ["Bloom filter", "Count-min sketch", "HyperLogLog", "False positive", "Space trade-off"]],
        ],
      },
      {
        n: "10",
        title: "Algorithms",
        summary:
          "Complexity analysis, searching, sorting, recursion, divide and conquer, greedy, dynamic programming, and graph algorithms.",
        sections: [
          ["10.1", "Complexity Analysis", ["Big O", "Big Omega", "Big Theta", "Time complexity", "Space complexity", "Real-world performance"]],
          ["10.2", "Searching", ["Linear search", "Binary search", "Hash lookup", "Tree search", "Graph search"]],
          ["10.3", "Sorting", ["Bubble sort", "Selection sort", "Insertion sort", "Merge sort", "Quick sort", "Heap sort", "Stable sort"]],
          ["10.4", "Algorithmic Patterns", ["Recursion", "Divide and conquer", "Greedy", "Dynamic programming", "Backtracking", "Two pointers", "Sliding window"]],
          ["10.5", "Graph Algorithms", ["BFS", "DFS", "Dijkstra", "Topological sort", "Minimum spanning tree", "Union find"]],
          ["10.6", "String Algorithms", ["Substring search", "Prefix table", "Trie search", "Edit distance", "Tokenization"]],
        ],
      },
    ],
  },
  {
    id: "part-iii",
    title: "Part III. Web And Application Engineering",
    chapters: [
      {
        n: "11",
        title: "Internet And Web Foundations",
        summary:
          "Network basics, DNS, URLs, HTTP, TLS, browsers, clients, servers, and request-response lifecycle.",
        sections: [
          ["11.1", "Network Basics", ["Host", "IP address", "Port", "Socket", "Packet", "Protocol", "Latency", "Bandwidth", "Throughput"]],
          ["11.2", "DNS And URLs", ["Domain", "DNS resolver", "Record", "URL", "Scheme", "Host", "Path", "Query", "Fragment"]],
          ["11.3", "HTTP And TLS", ["HTTP request", "HTTP response", "Header", "Body", "Status code", "Cookie", "TLS handshake", "Certificate"]],
          ["11.4", "Client And Server", ["Browser", "Server", "Static content", "Dynamic content", "Request lifecycle", "Response lifecycle"]],
        ],
      },
      {
        n: "12",
        title: "HTML, CSS, And JavaScript",
        summary:
          "The browser-native languages: document structure, presentation, behavior, DOM, events, and async work.",
        sections: [
          ["12.1", "HTML", ["Document", "Element", "Attribute", "Semantic HTML", "Form", "Input", "Table", "Accessibility"]],
          ["12.2", "CSS", ["Cascade", "Specificity", "Box model", "Display", "Position", "Flexbox", "Grid", "Responsive design", "SCSS"]],
          ["12.3", "JavaScript Runtime", ["Value", "Object", "Array", "Function", "Prototype", "Module", "Event loop", "Promise", "Async await"]],
          ["12.4", "DOM And Browser APIs", ["DOM tree", "Query selector", "Event", "Fetch", "Storage", "History", "Canvas", "Web worker"]],
        ],
      },
      {
        n: "13",
        title: "TypeScript And Frontend Engineering",
        summary:
          "TypeScript type system, modules, build tools, architecture, state, forms, accessibility, and tests.",
        sections: [
          ["13.1", "TypeScript Type System", ["Type annotation", "Interface", "Type alias", "Union", "Intersection", "Generic", "Narrowing", "Utility type"]],
          ["13.2", "Frontend Tooling", ["Package manager", "Bundler", "Vite", "Transpiler", "Linter", "Formatter", "Dev server", "Build output"]],
          ["13.3", "Frontend Architecture", ["Feature structure", "Component boundary", "API layer", "State management", "Routing", "Forms", "Validation", "Testing"]],
          ["13.4", "Accessibility And UX States", ["Keyboard navigation", "ARIA", "Loading state", "Empty state", "Error state", "Disabled state", "Focus management"]],
        ],
      },
      {
        n: "14",
        title: "React And UI Systems",
        summary:
          "Components, JSX, props, state, effects, hooks, rendering, reconciliation, performance, and design systems.",
        sections: [
          ["14.1", "React Fundamentals", ["Component", "JSX", "Props", "State", "Event", "Conditional rendering", "List rendering"]],
          ["14.2", "Hooks And Effects", ["useState", "useEffect", "useMemo", "useCallback", "useRef", "Custom hook", "Effect cleanup"]],
          ["14.3", "Rendering Internals", ["Virtual DOM", "Reconciliation", "Render phase", "Commit phase", "Batching", "Keys", "Strict mode"]],
          ["14.4", "UI Systems", ["Design token", "Component library", "Theme", "Layout primitive", "Form control", "Table", "Modal", "Toast"]],
          ["14.5", "React Performance", ["Unnecessary render", "Memoization", "Code splitting", "Lazy loading", "Profiler", "State colocation"]],
        ],
      },
      {
        n: "15",
        title: "Backend Engineering",
        summary:
          "Servers, routes, middleware, controllers, services, repositories, APIs, auth, background jobs, errors, and logs.",
        sections: [
          ["15.1", "Backend Mental Model", ["Request", "Route", "Middleware", "Controller", "Service", "Repository", "Database", "Response"]],
          ["15.2", "API Design", ["REST", "Resource", "HTTP method", "Status code", "Request body", "Response body", "Pagination", "Filtering", "Versioning"]],
          ["15.3", "Authentication And Authorization", ["Identity", "Credential", "Session", "Cookie", "JWT", "OAuth", "Role", "Permission", "Policy"]],
          ["15.4", "Backend Reliability", ["Validation", "Error handling", "Logging", "Retry", "Timeout", "Rate limit", "Background job", "Idempotency"]],
        ],
      },
    ],
  },
  {
    id: "part-iv",
    title: "Part IV. Data And Systems",
    chapters: [
      {
        n: "16",
        title: "Databases",
        summary:
          "Files to databases, relational model, SQL, indexes, transactions, query planning, storage, replication, NoSQL, caching, and search.",
        sections: [
          ["16.1", "Files To Databases", ["Memory", "Text file", "CSV", "JSON", "SQLite", "DBMS", "Client-server database"]],
          ["16.2", "Relational Model", ["Table", "Row", "Column", "Primary key", "Foreign key", "Constraint", "Relationship", "Normalization"]],
          ["16.3", "SQL", ["SELECT", "INSERT", "UPDATE", "DELETE", "JOIN", "GROUP BY", "HAVING", "Subquery", "Window function"]],
          ["16.4", "Indexes", ["B-tree index", "Hash index", "Composite index", "Covering index", "Selectivity", "Index scan", "Table scan"]],
          ["16.5", "Transactions", ["ACID", "Commit", "Rollback", "Isolation level", "Lock", "MVCC", "Deadlock", "WAL"]],
          ["16.6", "Query Planning And Storage", ["Parser", "Planner", "Optimizer", "Execution engine", "Buffer pool", "Storage engine", "Execution plan"]],
          ["16.7", "NoSQL, Cache, And Search", ["Document database", "Key-value store", "Column store", "Graph database", "Redis", "Elasticsearch", "Cache invalidation"]],
        ],
      },
      {
        n: "17",
        title: "Networking Deep Dive",
        summary:
          "IP, TCP, UDP, sockets, TLS, HTTP versions, WebSocket, and network debugging.",
        sections: [
          ["17.1", "IP And Routing", ["IP address", "Subnet", "Gateway", "Router", "NAT", "Packet", "TTL", "Traceroute"]],
          ["17.2", "TCP And UDP", ["TCP handshake", "Sequence number", "ACK", "Retransmission", "Congestion control", "UDP datagram", "Packet loss"]],
          ["17.3", "Sockets And TLS", ["Socket", "Bind", "Listen", "Accept", "Connect", "TLS handshake", "Certificate", "Cipher suite"]],
          ["17.4", "HTTP Deep Dive", ["HTTP/1.1", "HTTP/2", "HTTP/3", "Header compression", "Multiplexing", "WebSocket", "Streaming"]],
          ["17.5", "Network Debugging", ["ping", "traceroute", "nslookup", "curl", "netstat", "tcpdump", "Wireshark", "Browser Network tab"]],
        ],
      },
      {
        n: "18",
        title: "Distributed Systems",
        summary:
          "Partial failure, timeout, retry, idempotency, queues, pub/sub, consistency, replication, partitioning, CAP, consensus, and system design.",
        sections: [
          ["18.1", "Distributed Foundations", ["Network boundary", "Partial failure", "Timeout", "Retry", "Backoff", "Idempotency", "Circuit breaker"]],
          ["18.2", "Communication", ["Synchronous call", "Asynchronous message", "Message queue", "Pub/sub", "Event bus", "Streaming", "gRPC"]],
          ["18.3", "Distributed Data", ["Replication", "Partitioning", "Consistency", "Availability", "CAP theorem", "Eventual consistency", "Consensus"]],
          ["18.4", "System Design", ["Load balancing", "Caching", "CDN", "Rate limiting", "Search", "Queue-based scaling", "Database scaling"]],
        ],
      },
    ],
  },
  {
    id: "part-v",
    title: "Part V. Software Engineering In Production",
    chapters: [
      {
        n: "19",
        title: "Software Engineering",
        summary:
          "Requirements, domain understanding, code quality, testing, debugging, refactoring, documentation, and review.",
        sections: [
          ["19.1", "Requirements", ["Business problem", "User problem", "Functional requirement", "Non-functional requirement", "Constraint", "Acceptance criteria"]],
          ["19.2", "Code Quality", ["Readability", "Naming", "Duplication", "Coupling", "Cohesion", "Refactoring", "Technical debt"]],
          ["19.3", "Testing", ["Unit test", "Integration test", "End-to-end test", "Contract test", "Regression test", "Test pyramid", "Test strategy"]],
          ["19.4", "Debugging", ["Symptom", "Reproduction", "Evidence", "Hypothesis", "Experiment", "Root cause", "Fix", "Postmortem"]],
          ["19.5", "Documentation And Review", ["README", "Design note", "ADR", "Pull request", "Code review", "Incident report"]],
        ],
      },
      {
        n: "20",
        title: "Software Architecture",
        summary:
          "Architecture decisions, application architecture, system architecture, DDD, and trade-offs.",
        sections: [
          ["20.1", "Architecture Foundations", ["Context", "Constraint", "Trade-off", "Decision", "Consequence", "ADR"]],
          ["20.2", "Application Architecture", ["Single file", "Module", "MVC", "MVVM", "Layered architecture", "Clean architecture", "Hexagonal architecture"]],
          ["20.3", "System Architecture", ["Monolith", "Modular monolith", "SOA", "Microservices", "Event-driven architecture", "Serverless"]],
          ["20.4", "Domain-Driven Design", ["Domain", "Subdomain", "Bounded context", "Entity", "Value object", "Aggregate", "Domain event", "Repository"]],
        ],
      },
      {
        n: "21",
        title: "DevOps And Cloud",
        summary:
          "Git, branching, CI/CD, artifacts, containers, cloud compute, load balancers, CDN, managed services, and deployment strategies.",
        sections: [
          ["21.1", "Git And Collaboration", ["Repository", "Commit", "Branch", "Merge", "Rebase", "Pull request", "Code review", "Release branch"]],
          ["21.2", "CI/CD", ["Pipeline", "Build", "Test", "Artifact", "Deploy", "Rollback", "Environment promotion"]],
          ["21.3", "Containers", ["Docker", "Image", "Container", "Dockerfile", "Volume", "Network", "Compose", "Registry"]],
          ["21.4", "Cloud", ["VM", "VPS", "Load balancer", "Object storage", "Managed database", "CDN", "Serverless", "Region", "Availability zone"]],
          ["21.5", "Deployment Strategies", ["Blue-green", "Canary", "Rolling deployment", "Feature flag", "Rollback", "Migration strategy"]],
        ],
      },
      {
        n: "22",
        title: "Security",
        summary:
          "Threat modeling, auth security, web attacks, secrets, encryption, secure logging, and dependency security.",
        sections: [
          ["22.1", "Security Foundations", ["Threat", "Vulnerability", "Risk", "Attack surface", "Defense in depth", "Least privilege"]],
          ["22.2", "Web Security", ["SQL injection", "XSS", "CSRF", "CORS misconfiguration", "Broken authentication", "Broken authorization", "IDOR"]],
          ["22.3", "Application Security", ["Input validation", "Output encoding", "Secrets management", "Password hashing", "Encryption", "Secure logging", "Dependency security"]],
          ["22.4", "Operational Security", ["Patch management", "Audit log", "Access review", "Incident response", "Backup", "Disaster recovery"]],
        ],
      },
      {
        n: "23",
        title: "Performance And Observability",
        summary:
          "Resources, queues, contention, bottlenecks, profiling, logs, metrics, traces, dashboards, alerts, and incidents.",
        sections: [
          ["23.1", "Performance Foundations", ["Work", "Resource", "Queue", "Contention", "Latency", "Throughput", "Bottleneck"]],
          ["23.2", "Performance Resources", ["CPU", "Memory", "Disk", "Network", "Database", "Lock", "Thread", "Connection"]],
          ["23.3", "Profiling", ["Browser profiler", "Backend profiler", "Database plan", "Memory profiler", "Flame graph", "Benchmark"]],
          ["23.4", "Observability", ["Log", "Metric", "Trace", "Dashboard", "Alert", "SLO", "Incident", "Postmortem"]],
        ],
      },
    ],
  },
  {
    id: "part-vi",
    title: "Part VI. AI-Era Engineering",
    chapters: [
      {
        n: "24",
        title: "AI Foundations",
        summary:
          "AI, ML, DL, datasets, models, training, inference, evaluation, and product-level AI thinking.",
        sections: [
          ["24.1", "AI Mental Model", ["AI", "Machine learning", "Deep learning", "Model", "Dataset", "Training", "Inference", "Evaluation"]],
          ["24.2", "Data And Evaluation", ["Feature", "Label", "Train set", "Validation set", "Test set", "Metric", "Bias", "Drift"]],
          ["24.3", "AI Product Thinking", ["Use case", "Human-in-the-loop", "Failure cost", "Safety boundary", "Evaluation harness", "Feedback loop"]],
        ],
      },
      {
        n: "25",
        title: "Math For AI",
        summary:
          "Vectors, matrices, linear transformations, probability, statistics, gradients, and optimization.",
        sections: [
          ["25.1", "Linear Algebra", ["Scalar", "Vector", "Matrix", "Dot product", "Linear transformation", "Projection", "Embedding space"]],
          ["25.2", "Probability And Statistics", ["Random variable", "Distribution", "Mean", "Variance", "Bayes intuition", "Sampling", "Confidence"]],
          ["25.3", "Optimization", ["Loss function", "Gradient", "Gradient descent", "Learning rate", "Local minimum", "Regularization"]],
        ],
      },
      {
        n: "26",
        title: "Machine Learning And Deep Learning",
        summary:
          "Regression, classification, clustering, neural networks, backpropagation, CNN, RNN, and transformers.",
        sections: [
          ["26.1", "Machine Learning", ["Regression", "Classification", "Clustering", "Feature engineering", "Overfitting", "Validation", "Metrics"]],
          ["26.2", "Neural Networks", ["Neuron", "Layer", "Activation", "Loss", "Backpropagation", "Optimizer", "Batch", "Epoch"]],
          ["26.3", "Deep Learning Architectures", ["CNN", "RNN", "Attention", "Transformer", "Encoder", "Decoder", "Fine-tuning"]],
        ],
      },
      {
        n: "27",
        title: "LLM Engineering",
        summary:
          "Tokens, context windows, prompting, structured output, embeddings, vector search, RAG, tools, agents, evaluation, and guardrails.",
        sections: [
          ["27.1", "LLM Basics", ["Token", "Context window", "Prompt", "Completion", "Temperature", "System message", "Instruction hierarchy"]],
          ["27.2", "Retrieval And Tools", ["Embedding", "Vector search", "Chunking", "RAG", "Tool calling", "Structured output", "Function schema"]],
          ["27.3", "Agents", ["Task decomposition", "Tool loop", "Memory", "Planning", "Execution", "Verification", "Human approval"]],
          ["27.4", "Evaluation And Guardrails", ["Golden set", "Regression eval", "Hallucination", "Safety boundary", "Policy check", "Observability"]],
        ],
      },
      {
        n: "28",
        title: "AI-Augmented Software Engineering",
        summary:
          "Using AI for specifications, architecture, coding, testing, debugging, review, documentation, and risk control.",
        sections: [
          ["28.1", "AI In The Engineering Workflow", ["Problem definition", "Specification", "Architecture", "Implementation", "Testing", "Documentation", "Review"]],
          ["28.2", "AI For Coding", ["Prompting for code", "Code review", "Test generation", "Refactoring", "Debugging", "Benchmarking"]],
          ["28.3", "Risks Of AI-Generated Code", ["Incorrect abstraction", "Security bug", "Hidden dependency", "Over-complexity", "Unverified claim", "License risk"]],
          ["28.4", "Human Verification", ["Acceptance criteria", "Static check", "Runtime check", "Visual check", "Benchmark", "Production monitoring"]],
        ],
      },
    ],
  },
  {
    id: "part-vii",
    title: "Part VII. Learning Paths, Projects, And Reference",
    chapters: [
      {
        n: "29",
        title: "Learning Paths",
        summary:
          "Curated paths through the library for bottom-up CS, web, frontend, backend, fullstack, DevOps, AI, and systems engineering.",
        sections: [
          ["29.1", "Computer Science From The Bottom Up", ["Bit to program", "Program to process", "Process to OS", "OS to network", "Network to web app"]],
          ["29.2", "Web From Scratch", ["HTML page", "CSS layout", "JavaScript interaction", "TypeScript refactor", "API integration", "Fullstack app"]],
          ["29.3", "Role Paths", ["Frontend path", "Backend path", "Fullstack path", "DevOps path", "AI engineering path", "Systems engineering path"]],
        ],
      },
      {
        n: "30",
        title: "Build Primitive Systems",
        summary:
          "Small implementations that break abstractions open and make invisible systems visible.",
        sections: [
          ["30.1", "Computer Primitives", ["Binary converter", "Logic gate simulator", "Toy CPU emulator", "Memory allocator"]],
          ["30.2", "OS And Network Primitives", ["Shell", "Pipe demo", "HTTP server", "TCP client/server", "Thread pool"]],
          ["30.3", "Application Primitives", ["Router", "Hash table", "Database index", "Cache", "Event bus", "Mini React renderer", "Neural network"]],
        ],
      },
      {
        n: "31",
        title: "Follow One Request Through The System",
        summary:
          "Trace one user action from click to pixels, across browser, network, backend, database, and rendering pipeline.",
        sections: [
          ["31.1", "Browser Side", ["User click", "DOM event", "JavaScript runtime", "Event loop", "Fetch", "Browser network stack"]],
          ["31.2", "Server Side", ["Server socket", "HTTP parser", "Backend route", "Middleware", "Application service", "Repository"]],
          ["31.3", "Database Side", ["Database driver", "SQL parser", "Query planner", "Execution engine", "Buffer pool", "Index", "Storage engine"]],
          ["31.4", "Return Path", ["HTTP response", "Browser receive", "State update", "React render", "Layout", "Paint", "Composite", "Pixel on screen"]],
        ],
      },
      {
        n: "32",
        title: "Reference Library",
        summary:
          "Glossary, bilingual vocabulary, cheat sheets, debugging commands, failure modes, ADRs, and reading list.",
        sections: [
          ["32.1", "Glossary", ["Computer science terms", "Programming terms", "Web terms", "Database terms", "Networking terms", "AI terms"]],
          ["32.2", "Vocabulary", ["English term", "IPA", "Vietnamese meaning", "Simple English meaning", "Word family", "Collocation", "Example sentence"]],
          ["32.3", "Cheat Sheets", ["Git", "Linux commands", "HTTP status codes", "SQL", "Regex", "Docker", "TypeScript", "React"]],
          ["32.4", "Operational Reference", ["Debugging commands", "Common failure modes", "ADR templates", "Reading list"]],
        ],
      },
    ],
  },
];

const chapters = parts.flatMap((part) =>
  part.chapters.map((chapter) => ({ ...chapter, partId: part.id, partTitle: part.title }))
);

function slug(chapter) {
  return `${chapter.n}-${chapter.title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")}.html`;
}

function esc(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function layout({ title, body, active = "" }) {
  const nav = chapters
    .map((chapter) => {
      const href = `chapters/${slug(chapter)}`;
      const cls = active === chapter.n ? "active" : "";
      return `<a class="${cls}" href="${active ? slug(chapter) : href}"><span>${chapter.n}</span>${esc(chapter.title)}</a>`;
    })
    .join("");

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${esc(title)}</title>
  <link rel="stylesheet" href="${active ? "../assets/styles.css" : "assets/styles.css"}">
</head>
<body>
  <aside class="sidebar">
    <a class="brand" href="${active ? "../index.html" : "index.html"}">
      <strong>Tech Forge</strong>
      <span>Learning Library</span>
    </a>
    <nav>${nav}</nav>
  </aside>
  <main class="page">
    ${body}
  </main>
</body>
</html>
`;
}

function renderIndex() {
  const partBlocks = parts
    .map((part) => {
      const chapterCards = part.chapters
        .map((chapter) => {
          const sectionList = chapter.sections
            .map(([num, title, lessons]) => `<li><strong>${num}</strong> ${esc(title)} <span>${lessons.length} lessons</span></li>`)
            .join("");
          return `<article class="chapter-card">
            <a class="chapter-title" href="chapters/${slug(chapter)}">${chapter.n}. ${esc(chapter.title)}</a>
            <p>${esc(chapter.summary)}</p>
            <ol>${sectionList}</ol>
          </article>`;
        })
        .join("");
      return `<section class="part" id="${part.id}">
        <div class="part-heading">
          <p class="eyebrow">${part.id === "intro" ? "Start here" : "Book part"}</p>
          <h2>${esc(part.title)}</h2>
        </div>
        <div class="chapter-grid">${chapterCards}</div>
      </section>`;
    })
    .join("");

  const body = `<header class="hero">
    <p class="eyebrow">Full HTML TOC</p>
    <h1>Tech Forge Learning Library</h1>
    <blockquote>
      <p>A learning library for Computer Science, Software Engineering, and AI-era engineering.</p>
      <p>Micro practice, macro vision. Learn from first principles. Build primitives. Understand systems. Use AI as leverage.</p>
    </blockquote>
    <div class="hero-stats">
      <span><strong>${parts.length}</strong> parts</span>
      <span><strong>${chapters.length}</strong> chapters</span>
      <span><strong>${chapters.reduce((sum, chapter) => sum + chapter.sections.length, 0)}</strong> sections</span>
      <span><strong>${chapters.reduce((sum, chapter) => sum + chapter.sections.reduce((s, section) => s + section[2].length, 0), 0)}</strong> lessons</span>
    </div>
  </header>
  <section class="manifesto">
    <h2>The Zen Of This Book</h2>
    <ul>
      <li>Start from the smallest primitive you can observe.</li>
      <li>Connect every abstraction to the problem that created it.</li>
      <li>Practice at the micro level, reason at the system level.</li>
      <li>Use AI to accelerate implementation, verification, and explanation.</li>
    </ul>
  </section>
  ${partBlocks}`;

  return layout({ title: "Tech Forge Learning Library", body });
}

function renderChapter(chapter, index) {
  const prev = chapters[index - 1];
  const next = chapters[index + 1];
  const sections = chapter.sections
    .map(([num, title, lessons]) => {
      const lessonCards = lessons
        .map((lesson, i) => {
          const lessonNum = `${num}.${i + 1}`;
          const lensItems = standardLens
            .map((lens) => `<li><strong>${lens}:</strong> ${lessonSentence(lens, lesson, chapter.title)}</li>`)
            .join("");
          return `<article class="lesson-card" id="${lessonNum.replaceAll(".", "-")}">
            <h4>${lessonNum}. ${esc(lesson)}</h4>
            <ul>${lensItems}</ul>
          </article>`;
        })
        .join("");
      return `<section class="detail-section" id="${num.replaceAll(".", "-")}">
        <div class="section-heading">
          <p class="section-number">${num}</p>
          <h2>${esc(title)}</h2>
          <p>${sectionSummary(title, chapter.title)}</p>
        </div>
        <div class="lesson-grid">${lessonCards}</div>
      </section>`;
    })
    .join("");

  const sectionNav = chapter.sections
    .map(([num, title]) => `<a href="#${num.replaceAll(".", "-")}">${num} ${esc(title)}</a>`)
    .join("");

  const body = `<header class="chapter-hero">
    <p class="eyebrow">${esc(chapter.partTitle)}</p>
    <h1>${chapter.n}. ${esc(chapter.title)}</h1>
    <p>${esc(chapter.summary)}</p>
    <div class="chapter-actions">
      <a href="../index.html">Back to TOC</a>
      ${prev ? `<a href="${slug(prev)}">Previous: ${prev.n}</a>` : ""}
      ${next ? `<a href="${slug(next)}">Next: ${next.n}</a>` : ""}
    </div>
  </header>
  <section class="chapter-map">
    <h2>Chapter Map</h2>
    <nav>${sectionNav}</nav>
  </section>
  ${sections}`;

  return layout({ title: `${chapter.n}. ${chapter.title}`, body, active: chapter.n });
}

function lessonSentence(lens, lesson, chapterTitle) {
  const lower = lesson.toLowerCase();
  const variants = {
    "Concept": `Define ${esc(lesson)} in the context of ${esc(chapterTitle)} using simple language and one concrete example.`,
    "Problem it solves": `Explain what becomes painful or impossible before ${esc(lower)} exists.`,
    "Primitive model": `Build the smallest possible version or simulation that reveals the core idea.`,
    "Under the hood": `Trace the hidden mechanism, data movement, runtime behavior, and important boundaries.`,
    "Practice": `Complete a short exercise that turns the idea into code, a diagram, or a debugging note.`,
    "Debug / observe": `Use visible evidence such as logs, DevTools, profiler output, shell commands, memory views, or execution plans.`,
    "Trade-offs": `Compare speed, memory, complexity, correctness, security, and maintainability costs.`,
    "AI-aware engineering": `Use AI to generate hypotheses or examples, then verify with evidence instead of trusting the answer blindly.`,
  };
  return variants[lens];
}

function sectionSummary(sectionTitle, chapterTitle) {
  return `This section studies ${esc(sectionTitle)} as part of ${esc(chapterTitle)}. Each lesson keeps the same learning loop: understand the concept, rebuild the primitive, observe the internals, break it, and compare trade-offs.`;
}

function styles() {
  return `:root {
  --bg: #f7f5ef;
  --panel: #ffffff;
  --ink: #1f2933;
  --muted: #667085;
  --line: #d9d3c4;
  --accent: #0f766e;
  --accent-2: #7c3aed;
  --code: #102a43;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: var(--ink);
  background: var(--bg);
  line-height: 1.55;
}
a { color: inherit; }
.sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  width: 310px;
  overflow: auto;
  border-right: 1px solid var(--line);
  background: #fbfaf6;
  padding: 22px 18px;
}
.brand {
  display: grid;
  gap: 2px;
  text-decoration: none;
  margin-bottom: 18px;
}
.brand strong { font-size: 1.1rem; }
.brand span { color: var(--muted); font-size: .9rem; }
.sidebar nav {
  display: grid;
  gap: 4px;
}
.sidebar nav a {
  display: grid;
  grid-template-columns: 38px 1fr;
  gap: 8px;
  align-items: baseline;
  padding: 8px 9px;
  border-radius: 8px;
  text-decoration: none;
  color: #344054;
  font-size: .9rem;
}
.sidebar nav a:hover,
.sidebar nav a.active {
  background: #e7f4f1;
  color: #0f5f59;
}
.sidebar nav span {
  font-variant-numeric: tabular-nums;
  color: var(--accent);
  font-weight: 700;
}
.page {
  margin-left: 310px;
  min-height: 100vh;
  padding: 42px clamp(24px, 5vw, 72px);
}
.hero,
.chapter-hero,
.manifesto,
.chapter-map,
.part,
.detail-section {
  max-width: 1180px;
  margin: 0 auto 28px;
}
.hero,
.chapter-hero {
  padding: clamp(30px, 5vw, 62px) 0 28px;
}
.eyebrow {
  color: var(--accent);
  font-size: .8rem;
  font-weight: 800;
  letter-spacing: .08em;
  text-transform: uppercase;
  margin: 0 0 8px;
}
h1 {
  font-size: clamp(2.2rem, 5vw, 4.8rem);
  line-height: 1;
  letter-spacing: 0;
  margin: 0 0 18px;
}
h2 {
  font-size: clamp(1.5rem, 3vw, 2.4rem);
  margin: 0 0 10px;
  letter-spacing: 0;
}
h3, h4 { letter-spacing: 0; }
blockquote {
  margin: 20px 0;
  padding-left: 18px;
  border-left: 4px solid var(--accent);
  color: #344054;
  max-width: 850px;
}
.hero-stats,
.chapter-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 22px;
}
.hero-stats span,
.chapter-actions a,
.chapter-map a {
  border: 1px solid var(--line);
  background: var(--panel);
  border-radius: 8px;
  padding: 9px 12px;
  text-decoration: none;
}
.manifesto,
.chapter-map {
  background: #102a43;
  color: white;
  border-radius: 14px;
  padding: 28px;
}
.manifesto ul {
  display: grid;
  gap: 8px;
  margin: 16px 0 0;
  padding-left: 20px;
}
.part-heading {
  padding: 20px 0 8px;
  border-top: 1px solid var(--line);
}
.chapter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
  gap: 16px;
}
.chapter-card,
.lesson-card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 18px;
  box-shadow: 0 1px 0 rgba(16, 42, 67, .04);
}
.chapter-title {
  display: inline-block;
  color: var(--code);
  font-size: 1.1rem;
  font-weight: 800;
  text-decoration: none;
  margin-bottom: 8px;
}
.chapter-card p,
.section-heading p,
.chapter-hero p {
  color: var(--muted);
}
.chapter-card ol {
  margin: 12px 0 0;
  padding-left: 21px;
}
.chapter-card li {
  margin: 7px 0;
}
.chapter-card li span {
  color: var(--muted);
  font-size: .85rem;
}
.chapter-map nav {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.chapter-map a {
  color: white;
  background: rgba(255,255,255,.08);
  border-color: rgba(255,255,255,.22);
}
.detail-section {
  padding-top: 18px;
}
.section-heading {
  margin-bottom: 14px;
}
.section-number {
  color: var(--accent-2);
  font-weight: 800;
  margin: 0 0 6px;
}
.lesson-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 14px;
}
.lesson-card h4 {
  margin: 0 0 10px;
  color: var(--code);
}
.lesson-card ul {
  margin: 0;
  padding-left: 19px;
}
.lesson-card li {
  margin: 8px 0;
  color: #475467;
}
.lesson-card strong {
  color: #101828;
}
@media (max-width: 900px) {
  .sidebar {
    position: static;
    width: auto;
    max-height: 320px;
    border-right: 0;
    border-bottom: 1px solid var(--line);
  }
  .page {
    margin-left: 0;
    padding: 26px 18px;
  }
  .chapter-grid,
  .lesson-grid {
    grid-template-columns: 1fr;
  }
}
`;
}

rmSync(outDir, { recursive: true, force: true });
mkdirSync(chapterDir, { recursive: true });
mkdirSync(assetDir, { recursive: true });
writeFileSync(join(assetDir, "styles.css"), styles(), "utf8");
writeFileSync(join(outDir, "index.html"), renderIndex(), "utf8");
writeFileSync(join(outDir, "toc.html"), renderIndex(), "utf8");
chapters.forEach((chapter, index) => {
  writeFileSync(join(chapterDir, slug(chapter)), renderChapter(chapter, index), "utf8");
});

console.log(`Generated ${chapters.length + 2} HTML files in ${outDir}`);
