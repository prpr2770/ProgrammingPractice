use std::cmp::max; 
use std::mem::{replace, swap};

#[derive{Debug, PartialEq, Clone}]
pub struct AVLNodeData<T:Ord> {
    pub value : T, 
    pub left: AVLTree<T>, 
    pub right: AVLTree<T>, 
    pub height: usize,

}

pub type AVLTree<T> = Option<Box<AVLNodeData<T>>>;

