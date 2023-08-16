use super::tree::{AVLNodeData, AVLTree};
use core::iter::Peekable; 
use std::cmp::Ordering; 
use std::iter::FromIterator; 
use std::mem::replace; 

#[derive(Debug, PartialEq, Clone)]
pub struct AVLTreeSet<T:Ord>{
    root: AVLTree<T>,
}

impl< 'a, T: 'a + Ord>< AVLTreeSet<T> {
    pub fn new() -> Self{
        Self {root:None}
    }


    fn tree_insert<T:Ord>(tree: &mut AVLTree<T>, value:T) -> bool{
        match tree{
            None => {
                *tree = Some(Box::new(
                    AVLNodeData{
                        value, 
                        left: None, 
                        right: None, 
                        height: 1,
                    }
                ));
                // mark complete, by returning true
                true
            },
            Some(node) => {
                let inserted = match node.value.cmp(&value){
                    Ordering::Equal => false, 
                    Ordering::Less => tree_insert(&mut node.right, value),
                    Ordering::Greater => tree_insert(&mut node.left, value),
                };

                //inserted;
            }
        }
    }

    pub fn insert(&mut self, value: T) -> bool {

        tree_insert(&mut self.root, value)
    }


}