'use client';

import { PanelResizeHandle } from 'react-resizable-panels';

/**
 * Styled divider for react-resizable-panels. `dir` is the direction of the PARENT
 * PanelGroup: a horizontal group needs a vertical (col-resize) bar; a vertical group
 * needs a horizontal (row-resize) bar. Hover/drag highlight is driven from globals.css
 * via the `amr-resize-handle` class + the library's data-resize-handle-state attribute.
 */
export function ResizeHandle({ dir = 'horizontal' }: { dir?: 'horizontal' | 'vertical' }) {
  const horizontal = dir === 'horizontal';
  return (
    <PanelResizeHandle
      className="amr-resize-handle"
      style={
        horizontal
          ? { width: 5, cursor: 'col-resize', flexShrink: 0 }
          : { height: 5, cursor: 'row-resize', flexShrink: 0 }
      }
    />
  );
}
