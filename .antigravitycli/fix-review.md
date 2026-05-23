---
name: fix-review
description: >
  Your task is to fix EVERY issue listed in the report by modifying the code of the referenced files. You must adapt your solutions perfectly to the paradigms and tools already used within each file.
---

Strictly follow these engineering rules:
1. Locate the exact file and line numbers specified in the report.
2. Fix high-priority bugs first, followed by architectural risks, and finally styling or idiomatic nits.
3. For backend integration and workers: Implement defensive error handling by checking content/response types before decoding payloads. Optimize resource allocation by streaming or chunking large data transfers instead of loading entire payloads into memory. Ensure system retries are only triggered for transient infrastructure errors, not permanent failures.
4. For data integrity and transactions: Ensure that side effects (such as persistence to external file storage or message queues) only occur after the database transaction is successfully committed. If an asynchronous operation or enqueueing fails, immediately update the state/status of the affected entity in the database to prevent stale records.
5. For security and validation: Never rely solely on client-side metadata for critical validations; implement deep verification on the server-side.
6. For frontend and user interface: Ensure asynchronous operations do not fail silently. Every exception must catch failures and trigger appropriate visual feedback or state updates for the user.
7. After applying the changes, you MUST provide a concise, step-by-step technical explanation of the architectural flow for each modification made.
