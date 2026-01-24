// Universal Core: Merkle Tree for Audit Evidence
// Provides cryptographic proof of audit log integrity

use sha2::{Sha256, Digest};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MerkleNode {
    pub hash: String,
    pub left: Option<Box<MerkleNode>>,
    pub right: Option<Box<MerkleNode>>,
    pub data: Option<String>, // Only leaf nodes have data
}

impl MerkleNode {
    pub fn leaf(hash: String, data: String) -> Self {
        Self {
            hash,
            left: None,
            right: None,
            data: Some(data),
        }
    }

    pub fn internal(left: Box<MerkleNode>, right: Option<Box<MerkleNode>>) -> Self {
        let mut hasher = Sha256::new();
        hasher.update(left.hash.as_bytes());
        if let Some(ref r) = right {
            hasher.update(r.hash.as_bytes());
        } else {
            // Duplicate left for odd nodes
            hasher.update(left.hash.as_bytes());
        }
        let hash = format!("{:x}", hasher.finalize());

        Self {
            hash,
            left: Some(left),
            right,
            data: None,
        }
    }
}

pub struct MerkleTree {
    root: Option<MerkleNode>,
    leaves: Vec<String>, // Record hashes
}

impl MerkleTree {
    pub fn new() -> Self {
        Self {
            root: None,
            leaves: Vec::new(),
        }
    }

    /// Build Merkle tree from audit record hashes
    pub fn from_hashes(hashes: Vec<String>) -> Self {
        if hashes.is_empty() {
            return Self::new();
        }

        let mut leaves: Vec<MerkleNode> = hashes
            .iter()
            .map(|h| MerkleNode::leaf(h.clone(), h.clone()))
            .collect();

        let root = Self::build_tree(&mut leaves);

        Self {
            root: Some(root),
            leaves: hashes,
        }
    }

    fn build_tree(nodes: &mut Vec<MerkleNode>) -> MerkleNode {
        if nodes.len() == 1 {
            return nodes.remove(0);
        }

        let mut next_level = Vec::new();
        for chunk in nodes.chunks(2) {
            let left = Box::new(chunk[0].clone());
            let right = if chunk.len() > 1 {
                Some(Box::new(chunk[1].clone()))
            } else {
                None
            };
            next_level.push(MerkleNode::internal(left, right));
        }

        Self::build_tree(&mut next_level)
    }

    /// Get Merkle root hash
    pub fn root_hash(&self) -> Option<String> {
        self.root.as_ref().map(|r| r.hash.clone())
    }

    /// Generate proof path for a specific leaf
    pub fn proof_path(&self, leaf_hash: &str) -> Option<Vec<String>> {
        if let Some(ref root) = self.root {
            Self::find_proof(root, leaf_hash, &mut Vec::new())
        } else {
            None
        }
    }

    fn find_proof(node: &MerkleNode, target: &str, path: &mut Vec<String>) -> Option<Vec<String>> {
        // If leaf node
        if node.left.is_none() && node.right.is_none() {
            if node.hash == target {
                return Some(path.clone());
            }
            return None;
        }

        // Check left subtree
        if let Some(ref left) = node.left {
            if let Some(mut proof) = Self::find_proof(left, target, path) {
                if let Some(ref right) = node.right {
                    proof.push(right.hash.clone());
                } else {
                    proof.push(left.hash.clone()); // Duplicate for odd nodes
                }
                return Some(proof);
            }
        }

        // Check right subtree
        if let Some(ref right) = node.right {
            if let Some(mut proof) = Self::find_proof(right, target, path) {
                if let Some(ref left) = node.left {
                    proof.push(left.hash.clone());
                }
                return Some(proof);
            }
        }

        None
    }

    /// Verify a leaf against root using proof path
    pub fn verify_proof(leaf_hash: &str, root_hash: &str, proof_path: &[String]) -> bool {
        let mut current = leaf_hash.to_string();
        for sibling in proof_path {
            let mut hasher = Sha256::new();
            // Order matters - use lexicographic ordering
            if current < *sibling {
                hasher.update(current.as_bytes());
                hasher.update(sibling.as_bytes());
            } else {
                hasher.update(sibling.as_bytes());
                hasher.update(current.as_bytes());
            }
            current = format!("{:x}", hasher.finalize());
        }
        current == root_hash
    }
}

impl Default for MerkleTree {
    fn default() -> Self {
        Self::new()
    }
}
