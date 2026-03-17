import React, { useRef, useEffect, useState, useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

const GridVisualizer = ({ gridData }) => {
  const fgRef = useRef();
  const containerRef = useRef();
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    if (containerRef.current) {
      setDimensions({
        width: containerRef.current.offsetWidth,
        height: containerRef.current.offsetHeight
      });
    }

    const handleResize = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.offsetWidth,
          height: containerRef.current.offsetHeight
        });
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    if (fgRef.current && gridData?.nodes?.length) {
      fgRef.current.d3Force('charge').strength(-300);
      fgRef.current.d3Force('link').distance(60);
      // Let it settle then fit
      setTimeout(() => {
        if (fgRef.current) fgRef.current.zoomToFit(400, 20);
      }, 1000);
    }
  }, [gridData]);

  const paintNode = useCallback((node, ctx, globalScale) => {
    const isOverloaded = node.overloaded;
    const isSource = node.type === 'source';
    
    // Node styling
    const size = isSource ? 8 : (node.type === 'substation' ? 6 : 4);
    const color = isOverloaded ? '#f43f5e' : (isSource ? '#eab308' : '#38bdf8');
    
    // Draw outer glow if overloaded
    if (isOverloaded) {
      ctx.beginPath();
      ctx.arc(node.x, node.y, size * 2.5, 0, 2 * Math.PI, false);
      ctx.fillStyle = 'rgba(244, 63, 94, 0.2)';
      ctx.fill();
    }
    
    // Draw node core
    ctx.beginPath();
    ctx.arc(node.x, node.y, size, 0, 2 * Math.PI, false);
    ctx.fillStyle = color;
    ctx.fill();
    
    // Draw label
    const label = node.label || node.id;
    const fontSize = 12 / globalScale;
    ctx.font = `${fontSize}px Sans-Serif`;
    const textWidth = ctx.measureText(label).width;
    const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding

    ctx.fillStyle = 'rgba(15, 23, 42, 0.8)';
    ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - size - bckgDimensions[1] - 4, ...bckgDimensions);

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#cbd5e1';
    ctx.fillText(label, node.x, node.y - size - bckgDimensions[1]/2 - 4);
    
    // Draw load indicator
    if (node.current_load > 0) {
      const loadText = `${node.current_load}MW`;
      ctx.fillStyle = isOverloaded ? '#fca5a5' : '#7dd3fc';
      ctx.fillText(loadText, node.x, node.y + size + fontSize);
    }
  }, []);

  const linkColor = useCallback((link) => {
    return link.overloaded ? 'rgba(244, 63, 94, 0.6)' : 'rgba(148, 163, 184, 0.3)';
  }, []);

  const linkWidth = useCallback((link) => {
    return (link.current_flow / 50) + 1;
  }, []);

  if (!gridData || !gridData.nodes || gridData.nodes.length === 0) {
    return (
      <div className="flex h-full w-full items-center justify-center text-slate-500">
        No grid data available
      </div>
    );
  }

  return (
    <div ref={containerRef} className="h-full w-full overflow-hidden bg-slate-900/50 rounded-xl relative">
      <div className="absolute top-4 left-4 z-10 flex gap-4">
        <div className="flex items-center gap-2 text-xs">
          <span className="w-3 h-3 rounded-full bg-yellow-500"></span> Source
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span className="w-3 h-3 rounded-full bg-sky-400"></span> Substation
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span className="w-3 h-3 rounded-full bg-rose-500 shadow-[0_0_10px_rgba(244,63,94,0.6)]"></span> Overloaded
        </div>
      </div>
      
      {dimensions.width > 0 && dimensions.height > 0 && (
        <ForceGraph2D
          ref={fgRef}
          width={dimensions.width}
          height={dimensions.height}
          graphData={gridData}
          nodeCanvasObject={paintNode}
          linkColor={linkColor}
          linkWidth={linkWidth}
          linkDirectionalParticles={(link) => (link.current_flow > 0 ? 2 : 0)}
          linkDirectionalParticleSpeed={(link) => link.current_flow * 0.001}
          linkDirectionalParticleWidth={2}
          linkDirectionalParticleColor={(link) => link.overloaded ? '#f43f5e' : '#38bdf8'}
          enableNodeDrag={true}
          enableZoom={true}
        />
      )}
    </div>
  );
};

export default GridVisualizer;
