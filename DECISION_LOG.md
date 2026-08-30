# Decision Log

## 1. Integration Approach

I chose the Monday.com API rather than hardcoding the provided CSV data.
The application retrieves Deals and Work Orders data dynamically from
Monday.com at request time.

This satisfies the read-only integration requirement and ensures that
responses reflect the current board data.

## 2. Technology Choice

I used Python with FastAPI because it provides a lightweight API layer,
simple request handling, automatic API documentation through Swagger,
and is suitable for rapid development within the six-hour assignment
constraint.

Requests is used for communication with the Monday.com GraphQL API.

The prototype is deployed on Render so that it can be tested without
local setup.

## 3. Query Understanding

The agent uses the user's natural-language question to determine the
requested business metric, such as:

- Deal counts
- Deal status
- Deal value
- Sector performance
- Work order counts
- Work order status
- Work order value
- Pipeline health
- Data quality

For ambiguous queries, the implementation can be extended with explicit
clarifying questions.

## 4. Data Resilience

The source data contains incomplete and inconsistent records.

The implementation therefore:

- Handles missing values
- Handles missing status fields
- Handles empty fields
- Converts numeric strings into numbers
- Removes commas from financial values before calculation
- Avoids crashing when individual records contain invalid numeric values
- Reports data-quality issues where appropriate

Financial and status-based results may therefore be affected when source
records are incomplete.

## 5. Business Intelligence

The goal was not only to return raw records but to provide business-level
answers.

Examples include:

- Pipeline health
- Win rate
- Dead deal rate
- Sector comparisons
- Highest-value sectors
- Work order operational metrics
- Data quality summaries

## 6. Leadership Updates

I interpreted "leadership updates" as concise summaries that help a
founder or executive understand the current business position without
manually inspecting Monday.com.

The agent therefore supports summaries containing pipeline metrics,
deal performance, operational work-order metrics, sector performance,
and relevant data-quality caveats.

## 7. Trade-offs

Given the six-hour development constraint, I prioritized:

1. Reliable Monday.com integration
2. Core business questions
3. Data-quality handling
4. API deployment
5. Simple conversational querying

A more sophisticated natural-language/LLM query planner was not
prioritized because reliable core functionality was more important for
the prototype.

## 8. Future Improvements

With additional time I would add:

- Advanced date and quarter filtering
- More robust natural-language interpretation
- Automatic clarification questions
- More comprehensive data normalization
- Retry and timeout strategies
- Visual dashboards
- Automated leadership-report generation
- Unit tests and integration tests
- Caching for frequently requested metrics
