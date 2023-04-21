import FabricTool, { ConfigureCanvasProps } from "./fabrictool"

class TransformTool extends FabricTool {
  configureCanvas(args: ConfigureCanvasProps): () => void {
    let canvas = this._canvas
    canvas.isDrawingMode = false
    canvas.selection = true
    canvas.forEachObject((o) => (o.selectable = o.evented = o.lockMovementX = o.lockMovementY =true))
    canvas.forEachObject((o) => (o.hasControls =false))

    const handleLeftClick = () => {
      const activeObject = canvas.getActiveObject()
      if (activeObject && activeObject.selectable) {
        activeObject.set({fill: 'rgb(1, 50, 32, 0.2)', stroke: 'rgb(50,205,50)'})
        canvas.renderAll()
      }
    }
    const handleRightClick = () => {
      const activeObject = canvas.getActiveObject()
      if (activeObject && activeObject.selectable) {
        activeObject.set({ fill: 'rgb(208, 240, 192, 0.2)', stroke: 'rgb(50,205,50)'})
        canvas.renderAll()
      }
    }
    const handleMouseDown = (options: fabric.IEvent) => {
      // Check if it's a left-click (0) or right-click (2) event
      const mouseEvent = options.e as MouseEvent;
      console.log(mouseEvent.button)
      if (mouseEvent.button === 0) {
        handleLeftClick()
      }
      else if (mouseEvent.button === 2) {
        handleRightClick()
      }
    }
     const handleSelection = () => {
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
    canvas.on({'mouse:down': handleMouseDown, 'selection:created': handleSelection})
    return () => {
      canvas.off({'mouse:down': handleMouseDown, 'selection:created': handleSelection})
    }
  }
}

export default TransformTool




