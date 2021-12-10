import { TreeNode } from '../types';

export const findPathInTree = (nodeId: number, parent: TreeNode): TreeNode[] => {
    const stack = [[parent, [parent] as TreeNode[]]];
    while (stack.length) {
        const [node, path]: [TreeNode, TreeNode[]] = stack.pop() as [TreeNode, TreeNode[]];
        if (node.id === nodeId) {
            return path;
        }
        if (node.children) {
            stack.push(...node.children.map((node: TreeNode) => [node, [...path, node]]));
        }
    }
    return [];
};
