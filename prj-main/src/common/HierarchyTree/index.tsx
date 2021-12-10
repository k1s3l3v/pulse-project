import { Tree, TreeNode } from '../types';
import toggleExpandIcon from '../assets/person_menu_blue.svg';
import toggleExpandIcon_dark from '../assets/person_menu.svg';
import './index.scss';
import { useEffect, useState } from 'react';
import { findPathInTree } from './TreeUtils';

const Branch = ({
    item,
    selectCallback,
    openAddChildModal,
    selected,
    path,
}: {
    item: TreeNode;
    selectCallback: (s: TreeNode) => void;
    openAddChildModal: (s: TreeNode) => void;
    selected: TreeNode;
    path: TreeNode[];
}) => {
    return (
        <div className="tree-branch">
            {item.children.map(el => {
                return (
                    <Node
                        item={el}
                        selected={selected}
                        selectCallback={selectCallback}
                        openAddChildModal={openAddChildModal}
                        key={el.id}
                        path={path}
                    />
                );
            })}
        </div>
    );
};

const Node = ({
    item,
    selected,
    selectCallback,
    openAddChildModal,
    path,
}: {
    item: TreeNode;
    selected: TreeNode;
    selectCallback: (s: TreeNode) => void;
    openAddChildModal: (s: TreeNode) => void;
    path: TreeNode[];
}) => {
    const [expand, setExpand] = useState<boolean>(!!path.find(el => el.id === item.id));

    useEffect(() => {
        setExpand(!!path.find(el => el.id === item.id));
    }, [path]);

    return (
        <div key={item.id} className="tree-node">
            {item.addable && (
                <span
                    onClick={() => {
                        openAddChildModal(item);
                    }}>{`➕ `}</span>
            )}
            <span
                className={`text-18 font-ptmono ${expand ? 'node-expanded' : 'weight-400'} ${
                    item.id === selected.id ? 'selected' : ''
                }`}
                onClick={() => {
                    selectCallback(item);
                }}>
                {item.name}
            </span>
            {item.children.length > 0 && (
                <img
                    src={toggleExpandIcon}
                    alt=""
                    className={expand ? 'expanded' : 'collapsed'}
                    onClick={() => {
                        setExpand(!expand);
                    }}
                />
            )}
            {expand && (
                <Branch
                    item={item}
                    selectCallback={selectCallback}
                    openAddChildModal={openAddChildModal}
                    selected={selected}
                    path={path}
                />
            )}
        </div>
    );
};

export const HierarchyTree = ({
    dataTree,
    onSelectedCallback,
    selectedNode,
    openAddChildModal,
}: {
    dataTree: Tree;
    onSelectedCallback: (el: TreeNode) => void;
    selectedNode: TreeNode;
    openAddChildModal: (el: TreeNode) => void;
}) => {
    const [path, setPath] = useState<TreeNode[]>(findPathInTree(selectedNode.id, dataTree.head));

    useEffect(() => {
        setPath(findPathInTree(selectedNode.id, dataTree.head));
    }, [selectedNode]);

    return (
        <div className="hierarchy-tree">
            <Node
                item={dataTree.head}
                selected={selectedNode}
                selectCallback={onSelectedCallback}
                openAddChildModal={openAddChildModal}
                path={path}
            />
        </div>
    );
};
