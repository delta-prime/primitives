"""Finding-related Cypher query templates.

All queries use $param placeholders. No string concatenation with user input.

Scope values: "cluster" for cluster-scope findings, "silo" for silo-scope.
"""

# Look up the prior :Finding for a cluster-scope (scope, cluster_id, silo_id)
# triple. Returns at most one row.
#
# Params:
#   scope       (str)  -- always "cluster"
#   cluster_id  (str)
#   silo_id     (str)
FETCH_CURRENT_FINDING_CLUSTER_SCOPE = """
MATCH (f:Finding {scope: $scope, cluster_id: $cluster_id, silo_id: $silo_id})
RETURN f.id AS id,
       f.version AS version,
       f.claims AS claims,
       f.summary AS summary,
       f.pass_id AS pass_id,
       f.quality_score AS quality_score
LIMIT 1
"""

# Look up the prior :Finding for a silo-scope (scope, silo_id) pair.
#
# Params:
#   scope    (str)  -- always "silo"
#   silo_id  (str)
FETCH_CURRENT_FINDING_SILO_SCOPE = """
MATCH (f:Finding {scope: $scope, silo_id: $silo_id})
WHERE f.cluster_id IS NULL
RETURN f.id AS id,
       f.version AS version,
       f.claims AS claims,
       f.summary AS summary,
       f.pass_id AS pass_id,
       f.quality_score AS quality_score
LIMIT 1
"""

# MERGE a cluster-scope :Finding and attach (:Finding)-[:ABOUT]->(:Cluster).
# MERGE key: (scope, cluster_id, silo_id).
#
# Params:
#   id                 (str)
#   scope              (str)      -- "cluster"
#   cluster_id         (str)
#   silo_id            (str)
#   org_id             (str)
#   pass_id            (str)
#   version            (int)
#   status             (str)      -- "draft"
#   summary_json       (str)
#   claims_json        (str)
#   inferred_json      (str)
#   member_fingerprint (str | None)
#   quality_score      (float)
#   visit_ref          (str | None)
#   source             (str)      -- "custodian"
#   model              (str | None)
#   created_at         (str)      -- ISO8601
#   updated_at         (str)      -- ISO8601
FINDING_MERGE_CLUSTER_SCOPE = """
MERGE (f:Finding {scope: $scope, cluster_id: $cluster_id, silo_id: $silo_id})
ON CREATE SET
    f.id = $id,
    f.created_at = $created_at
SET f.org_id = $org_id,
    f.pass_id = $pass_id,
    f.version = $version,
    f.status = $status,
    f.summary = $summary_json,
    f.claims = $claims_json,
    f.inferred_relations = $inferred_json,
    f.member_fingerprint = $member_fingerprint,
    f.quality_score = $quality_score,
    f.visit_ref = $visit_ref,
    f.needs_refresh = false,
    f.source = $source,
    f.model = $model,
    f.updated_at = $updated_at
WITH f
MATCH (c:Cluster {id: $cluster_id})
MERGE (f)-[:ABOUT]->(c)
RETURN f.id AS id, f.version AS version
"""

# MERGE a silo-scope :Finding and attach (:Finding)-[:SUMMARIZES]->(:Silo).
# MERGE key: (scope, silo_id); cluster_id stays null.
#
# Params: same as FINDING_MERGE_CLUSTER_SCOPE minus cluster_id.
FINDING_MERGE_SILO_SCOPE = """
MERGE (f:Finding {scope: $scope, silo_id: $silo_id})
ON CREATE SET
    f.id = $id,
    f.created_at = $created_at,
    f.cluster_id = null
SET f.org_id = $org_id,
    f.pass_id = $pass_id,
    f.version = $version,
    f.status = $status,
    f.summary = $summary_json,
    f.claims = $claims_json,
    f.inferred_relations = $inferred_json,
    f.member_fingerprint = $member_fingerprint,
    f.quality_score = $quality_score,
    f.visit_ref = $visit_ref,
    f.needs_refresh = false,
    f.source = $source,
    f.model = $model,
    f.updated_at = $updated_at
WITH f
MATCH (s:Silo {id: $silo_id})
MERGE (f)-[:SUMMARIZES]->(s)
RETURN f.id AS id, f.version AS version
"""

# Create a :FindingHistory snapshot of the prior body and link via
# (:Finding)-[:SUPERSEDES]->(:FindingHistory). Run before FINDING_MERGE_*
# so the prior body is preserved.
#
# Params:
#   finding_id   (str)  -- the id returned by fetch_current_finding
#   pass_id      (str)  -- the *prior* finding's pass_id
#   summary      (str)  -- prior summary JSON string (as stored)
#   claims_hash  (str)  -- sha256 of the prior claims JSON
#   created_at   (str)  -- ISO8601; the snapshot's own timestamp
#   org_id       (str)
FINDING_HISTORY_CREATE = """
MATCH (f:Finding {id: $finding_id})
CREATE (h:FindingHistory {
    pass_id: $pass_id,
    summary: $summary,
    claims_hash: $claims_hash,
    created_at: $created_at,
    org_id: $org_id
})
CREATE (f)-[:SUPERSEDES]->(h)
RETURN h.pass_id AS pass_id
"""

# Trim :FindingHistory nodes for a finding to the most recent $keep entries.
# Older snapshots are DETACH DELETEd. Ordered by created_at DESC.
#
# Params:
#   finding_id (str)
#   keep       (int)  -- always 20 in v1
FINDING_HISTORY_TRIM = """
MATCH (f:Finding {id: $finding_id})-[:SUPERSEDES]->(h:FindingHistory)
WITH h ORDER BY h.created_at DESC
SKIP $keep
DETACH DELETE h
"""

__all__ = [
    "FETCH_CURRENT_FINDING_CLUSTER_SCOPE",
    "FETCH_CURRENT_FINDING_SILO_SCOPE",
    "FINDING_MERGE_CLUSTER_SCOPE",
    "FINDING_MERGE_SILO_SCOPE",
    "FINDING_HISTORY_CREATE",
    "FINDING_HISTORY_TRIM",
]
