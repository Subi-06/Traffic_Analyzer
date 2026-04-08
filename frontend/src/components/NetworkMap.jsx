import React, { useEffect, useRef } from 'react';
import { Network } from 'vis-network';

const NetworkMap = ({ topology, path, congestion }) => {
  const containerRef = useRef(null);
  const networkRef = useRef(null);

  useEffect(() => {
    if (!topology || !containerRef.current) return;

    const nodes = topology.nodes.map(node => ({
      ...node,
      color: path.includes(node.id) ? (congestion > 0.8 ? '#f44336' : '#4caf50') : '#97c2fc',
      size: path.includes(node.id) ? 30 : 25
    }));

    const edges = topology.edges.map(edge => {
      const isPath = false;
      for(let i=0; i<path.length-1; i++) {
        if((path[i] === edge.from && path[i+1] === edge.to) || (path[i] === edge.to && path[i+1] === edge.from)) {
           return { ...edge, color: { color: congestion > 0.8 ? '#f44336' : '#4caf50' }, width: 4 };
        }
      }
      return { ...edge, color: '#848484', width: 1 };
    });

    const data = { nodes, edges };
    const options = {
      nodes: { shape: 'dot', font: { size: 14 } },
      edges: { smooth: { type: 'continuous' } },
      physics: { enabled: true }
    };

    if (!networkRef.current) {
      networkRef.current = new Network(containerRef.current, data, options);
    } else {
      networkRef.current.setData(data);
    }
  }, [topology, path, congestion]);

  return <div ref={containerRef} style={{ height: '500px', border: '1px solid #ccc', borderRadius: '8px', background: '#f9f9f9' }} />;
};

export default NetworkMap;
