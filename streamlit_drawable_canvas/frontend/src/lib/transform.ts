import FabricTool, { ConfigureCanvasProps } from "./fabrictool"
import { fabric } from "fabric"

class TransformTool extends FabricTool {
  configureCanvas(args: ConfigureCanvasProps): () => void {
    let canvas = this._canvas
    canvas.isDrawingMode = false
    canvas.selection = true

    canvas.forEachObject((o) => (o.selectable = o.evented = o.lockMovementX = o.lockMovementY =true))
    canvas.forEachObject((o) => (o.hasControls = false))

    const handleClick = () => {
      const activeObject = canvas.getActiveObject()
      if (activeObject && activeObject.selectable) {
        activeObject.set({ fill: 'rgb(208, 240, 192, 0.2)', stroke: 'rgb(50,205,50)'})
        canvas.renderAll()
      }
    }

    const handleSelection = () => {
      const selection = new fabric.ActiveSelection(canvas.getActiveObjects(), {
        canvas: canvas,
        transparentCorners: true,
        hasControls: false,
        borderColor: 'rgb(208, 240, 192, 0)',
        cornerColor: 'rgb(208, 240, 192, 0)'
      });
      canvas.setActiveObject(selection);
      canvas.renderAll();
      const selectedObjects = canvas.getActiveObjects();
      if (selectedObjects.length > 0) {
        selectedObjects.forEach(function (arrayItem) {
          if (arrayItem.selectable) {
            arrayItem.set({ fill: 'rgb(208, 238, 192, 0.2)', stroke: 'rgb(50,205,50)'});
          }
        })
        selectedObjects[0].set({ fill: 'rgb(208, 237, 192, 0.2)', stroke: 'rgb(50,205,50)'})
        selectedObjects[selectedObjects.length -1].set({ fill: 'rgb(208, 239, 192, 0.2)', stroke: 'rgb(50,205,50)'})
      canvas.renderAll()
      }
    }

    canvas.on('selection:created', handleSelection)
    canvas.on("mouse:down", handleClick)
    return () => {
      canvas.off("mouse:down", handleClick)
      canvas.off('selection:created', handleSelection)
    }
  }
}

export default TransformTool
