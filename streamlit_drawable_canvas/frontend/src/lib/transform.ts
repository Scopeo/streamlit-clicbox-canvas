import FabricTool, { ConfigureCanvasProps } from "./fabrictool"

class TransformTool extends FabricTool {
  configureCanvas(args: ConfigureCanvasProps): () => void {
    let canvas = this._canvas
    canvas.isDrawingMode = false
    canvas.selection = true
    canvas.forEachObject((o) => (o.selectable = o.evented =true))
    canvas.forEachObject((o) => (o.hasControls =false))

    const handleLeftClick = () => {
      const activeObject = canvas.getActiveObject()
      if (activeObject && activeObject.selectable) {
        activeObject.set({fill: 'rgb(208, 239, 192, 0.2)', stroke: 'rgb(50,205,50)', lockMovementX: true, lockMovementY: true})
        canvas.renderAll()
      }
    }
    const handleRightClick = () => {
      const activeObject = canvas.getActiveObject()
      if (activeObject && activeObject.selectable) {
        activeObject.set({ fill: 'rgb(208, 240, 192, 0.2)', stroke: 'rgb(50,205,50)', lockMovementX: true, lockMovementY: true})
        canvas.renderAll()
      }
    }
    const handleMouseDown = (options: fabric.IEvent) => {
      // Check if it's a left-click (0) or right-click (2) event
      const mouseEvent = options.e as MouseEvent;
      if (mouseEvent.button === 0) {
        handleLeftClick()
      }
      else if (mouseEvent.button === 2) {
        handleRightClick()
      }
    }


     const handleSelection = (options: fabric.IEvent) => {
      const mouseEvent = options.e as MouseEvent;
      let color_click: string
      if (mouseEvent.button === 0) {
        color_click = 'rgb(208, 239, 192, 0.2)'
      }
      else {
        color_click = 'rgb(208, 240, 192, 0.2)'
      }
      const selectedObjects = canvas.getActiveObjects();
      if (selectedObjects.length > 1) {
        selectedObjects.forEach(function (arrayItem) {
          if (arrayItem.selectable) {
            arrayItem.set({ fill: color_click, stroke: 'rgb(50,200,50)'});
          }
        })
        selectedObjects[0].set({ fill: color_click, stroke: 'rgb(50,199,50)'})
        selectedObjects[selectedObjects.length -1].set({ fill: color_click, stroke: 'rgb(50,201,50)'})
      }
      if (selectedObjects.length === 1) {
        selectedObjects[0].set({ fill: color_click, stroke: 'rgb(50,205,50)'})
      }
      canvas.setActiveObject(selectedObjects[0])
      canvas.renderAll()
    }
    canvas.on({'mouse:down': handleMouseDown, 'selection:created': handleSelection})
    return () => {
      canvas.off({'mouse:down': handleMouseDown, 'selection:created': handleSelection})
    }
  }
}

export default TransformTool




