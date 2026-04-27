"""Pass ledger Cypher query templates.

All queries use $param placeholders. No string concatenation with user input.

:Pass nodes track Custodian pass lifecycle; :CLAIMED edges provide per-visit
idempotency within a pass.
"""

# Create a :Pass node with initial state.
#
# Params:
#   id         (str)
#   silo_id    (str)
#   org_id     (str)
#   status     (str)  -- "running"
#   started_at (str)  -- ISO8601
PASS_CREATE = """
CREATE (p:Pass {
    id: $id,
    silo_id: $silo_id,
    org_id: $org_id,
    status: $status,
    started_at: $started_at,
    finalized_at: null,
    cost_usd: 0.0,
    visit_count: 0
})
RETURN p.id AS id
"""

# Finalize a pass: set terminal status, finalized_at, accumulated cost, visit count.
#
# Params:
#   pass_id      (str)
#   status       (str)   -- terminal status
#   finalized_at (str)   -- ISO8601
#   cost_usd     (float)
#   visit_count  (int)
PASS_FINALIZE = """
MATCH (p:Pass {id: $pass_id})
SET p.status = $status,
    p.finalized_at = $finalized_at,
    p.cost_usd = $cost_usd,
    p.visit_count = $visit_count
RETURN p.id AS id
"""

# Check if a cluster is already CLAIMED in this pass (idempotency check).
#
# Params:
#   pass_id    (str)
#   cluster_id (str)
PASS_CHECK_CLAIMED = """
MATCH (p:Pass {id: $pass_id})-[:CLAIMED]->(c:Cluster {id: $cluster_id})
RETURN count(*) > 0 AS claimed
"""

# Fetch a :Pass node by id and org_id for org-isolated status reads.
#
# Params:
#   pass_id (str)
#   org_id  (str)
PASS_GET_BY_ID = """
MATCH (p:Pass {id: $pass_id, org_id: $org_id})
RETURN p.id AS id,
       p.silo_id AS silo_id,
       p.org_id AS org_id,
       p.status AS status,
       p.started_at AS started_at,
       p.finalized_at AS finalized_at,
       p.cost_usd AS cost_usd,
       p.visit_count AS visit_count
LIMIT 1
"""

# MERGE the (:Pass)-[:CLAIMED {claimed_at}]->(:Cluster) ledger edge.
# Transactionally consistent with the finding write in the same bolt transaction.
#
# Params:
#   pass_id    (str)
#   cluster_id (str)
#   claimed_at (str)  -- ISO8601
PASS_CLAIMED_EDGE_MERGE = """
MATCH (p:Pass {id: $pass_id})
MATCH (c:Cluster {id: $cluster_id})
MERGE (p)-[e:CLAIMED]->(c)
ON CREATE SET e.claimed_at = $claimed_at
RETURN e.claimed_at AS claimed_at
"""

__all__ = [
    "PASS_CREATE",
    "PASS_FINALIZE",
    "PASS_CHECK_CLAIMED",
    "PASS_GET_BY_ID",
    "PASS_CLAIMED_EDGE_MERGE",
]
