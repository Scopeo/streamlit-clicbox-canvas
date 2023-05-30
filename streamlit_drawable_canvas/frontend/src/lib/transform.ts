import FabricTool, { ConfigureCanvasProps } from "./fabrictool"

let color_list: string[] = [
"rgb(255, 0, 0, 0.2)",
"rgb(0, 255, 0, 0.2)",
"rgb(0, 0, 255, 0.2)",
"rgb(255, 255, 0, 0.2)",
"rgb(255, 0, 255, 0.2)",
"rgb(0, 255, 255, 0.2)",
"rgb(128, 0, 0, 0.2)",
"rgb(0, 128, 0, 0.2)",
"rgb(128, 128, 0, 0.2)",
"rgb(128, 0, 128, 0.2)",
"rgb(0, 128, 128, 0.2)",
"rgb(255, 128, 0, 0.2)",
"rgb(0, 255, 128, 0.2)",
"rgb(128, 0, 255, 0.2)",
"rgb(255, 0, 128, 0.2)",
"rgb(128, 255, 0, 0.2)",
"rgb(255, 128, 128, 0.2)",
"rgb(128, 128, 255, 0.2)",
"rgb(255, 0, 0, 0.21)",
"rgb(0, 255, 0, 0.21)",
"rgb(0, 0, 255, 0.21)",
"rgb(255, 255, 0, 0.21)",
"rgb(255, 0, 255, 0.21)",
"rgb(0, 255, 255, 0.21)",
"rgb(128, 0, 0, 0.21)",
"rgb(0, 128, 0, 0.21)",
"rgb(128, 128, 0, 0.21)",
"rgb(128, 0, 128, 0.21)",
"rgb(0, 128, 128, 0.21)",
"rgb(255, 128, 0, 0.21)",
"rgb(0, 255, 128, 0.21)",
"rgb(128, 0, 255, 0.21)",
"rgb(255, 0, 128, 0.21)",
"rgb(128, 255, 0, 0.21)",
"rgb(255, 128, 128, 0.21)",
"rgb(128, 128, 255, 0.21)",
"rgb(255, 0, 0, 0.22)",
"rgb(0, 255, 0, 0.22)",
"rgb(0, 0, 255, 0.22)",
"rgb(255, 255, 0, 0.22)",
"rgb(255, 0, 255, 0.22)",
"rgb(0, 255, 255, 0.22)",
"rgb(128, 0, 0, 0.22)",
"rgb(0, 128, 0, 0.22)",
"rgb(128, 128, 0, 0.22)",
"rgb(128, 0, 128, 0.22)",
"rgb(0, 128, 128, 0.22)",
"rgb(255, 128, 0, 0.22)",
"rgb(0, 255, 128, 0.22)",
"rgb(128, 0, 255, 0.22)",
"rgb(255, 0, 128, 0.22)",
"rgb(128, 255, 0, 0.22)",
"rgb(255, 128, 128, 0.22)",
"rgb(128, 128, 255, 0.22)",
"rgb(255, 0, 0, 0.23)",
"rgb(0, 255, 0, 0.23)",
"rgb(0, 0, 255, 0.23)",
"rgb(255, 255, 0, 0.23)",
"rgb(255, 0, 255, 0.23)",
"rgb(0, 255, 255, 0.23)",
"rgb(128, 0, 0, 0.23)",
"rgb(0, 128, 0, 0.23)",
"rgb(128, 128, 0, 0.23)",
"rgb(128, 0, 128, 0.23)",
"rgb(0, 128, 128, 0.23)",
"rgb(255, 128, 0, 0.23)",
"rgb(0, 255, 128, 0.23)",
"rgb(128, 0, 255, 0.23)",
"rgb(255, 0, 128, 0.23)",
"rgb(128, 255, 0, 0.23)",
"rgb(255, 128, 128, 0.23)",
"rgb(128, 128, 255, 0.23)",
"rgb(255, 0, 0, 0.24)",
"rgb(0, 255, 0, 0.24)",
"rgb(0, 0, 255, 0.24)",
"rgb(255, 255, 0, 0.24)",
"rgb(255, 0, 255, 0.24)",
"rgb(0, 255, 255, 0.24)",
"rgb(128, 0, 0, 0.24)",
"rgb(0, 128, 0, 0.24)",
"rgb(128, 128, 0, 0.24)",
"rgb(128, 0, 128, 0.24)",
"rgb(0, 128, 128, 0.24)",
"rgb(255, 128, 0, 0.24)",
"rgb(0, 255, 128, 0.24)",
"rgb(128, 0, 255, 0.24)",
"rgb(255, 0, 128, 0.24)",
"rgb(128, 255, 0, 0.24)",
"rgb(255, 128, 128, 0.24)",
"rgb(128, 128, 255, 0.24)",
"rgb(255, 0, 0, 0.25)",
"rgb(0, 255, 0, 0.25)",
"rgb(0, 0, 255, 0.25)",
"rgb(255, 255, 0, 0.25)",
"rgb(255, 0, 255, 0.25)",
"rgb(0, 255, 255, 0.25)",
"rgb(128, 0, 0, 0.25)",
"rgb(0, 128, 0, 0.25)",
"rgb(128, 128, 0, 0.25)",
"rgb(128, 0, 128, 0.25)",
"rgb(0, 128, 128, 0.25)",
"rgb(255, 128, 0, 0.25)",
"rgb(0, 255, 128, 0.25)",
"rgb(128, 0, 255, 0.25)",
"rgb(255, 0, 128, 0.25)",
"rgb(128, 255, 0, 0.25)",
"rgb(255, 128, 128, 0.25)",
"rgb(128, 128, 255, 0.25)"]


let stroke_list: string[] = [
"rgb(255, 0, 0)",
"rgb(0, 255, 0)",
"rgb(0, 0, 255)",
"rgb(255, 255, 0)",
"rgb(255, 0, 255)",
"rgb(0, 255, 255)",
"rgb(128, 0, 0)",
"rgb(0, 128, 0)",
"rgb(128, 128, 0)",
"rgb(128, 0, 128)",
"rgb(0, 128, 128)",
"rgb(255, 128, 0)",
"rgb(0, 255, 128)",
"rgb(128, 0, 255)",
"rgb(255, 0, 128)",
"rgb(128, 255, 0)",
"rgb(255, 128, 128)",
"rgb(128, 128, 255)",
"rgb(255, 0, 0)",
"rgb(0, 255, 0)",
"rgb(0, 0, 255)",
"rgb(255, 255, 0)",
"rgb(255, 0, 255)",
"rgb(0, 255, 255)",
"rgb(128, 0, 0)",
"rgb(0, 128, 0)",
"rgb(128, 128, 0)",
"rgb(128, 0, 128)",
"rgb(0, 128, 128)",
"rgb(255, 128, 0)",
"rgb(0, 255, 128)",
"rgb(128, 0, 255)",
"rgb(255, 0, 128)",
"rgb(128, 255, 0)",
"rgb(255, 128, 128)",
"rgb(128, 128, 255)",
"rgb(255, 0, 0)",
"rgb(0, 255, 0)",
"rgb(0, 0, 255)",
"rgb(255, 255, 0)",
"rgb(255, 0, 255)",
"rgb(0, 255, 255)",
"rgb(128, 0, 0)",
"rgb(0, 128, 0)",
"rgb(128, 128, 0)",
"rgb(128, 0, 128)",
"rgb(0, 128, 128)",
"rgb(255, 128, 0)",
"rgb(0, 255, 128)",
"rgb(128, 0, 255)",
"rgb(255, 0, 128)",
"rgb(128, 255, 0)",
"rgb(255, 128, 128)",
"rgb(128, 128, 255)",
"rgb(255, 0, 0)",
"rgb(0, 255, 0)",
"rgb(0, 0, 255)",
"rgb(255, 255, 0)",
"rgb(255, 0, 255)",
"rgb(0, 255, 255)",
"rgb(128, 0, 0)",
"rgb(0, 128, 0)",
"rgb(128, 128, 0)",
"rgb(128, 0, 128)",
"rgb(0, 128, 128)",
"rgb(255, 128, 0)",
"rgb(0, 255, 128)",
"rgb(128, 0, 255)",
"rgb(255, 0, 128)",
"rgb(128, 255, 0)",
"rgb(255, 128, 128)",
"rgb(128, 128, 255)",
"rgb(255, 0, 0)",
"rgb(0, 255, 0)",
"rgb(0, 0, 255)",
"rgb(255, 255, 0)",
"rgb(255, 0, 255)",
"rgb(0, 255, 255)",
"rgb(128, 0, 0)",
"rgb(0, 128, 0)",
"rgb(128, 128, 0)",
"rgb(128, 0, 128)",
"rgb(0, 128, 128)",
"rgb(255, 128, 0)",
"rgb(0, 255, 128)",
"rgb(128, 0, 255)",
"rgb(255, 0, 128)",
"rgb(128, 255, 0)",
"rgb(255, 128, 128)",
"rgb(128, 128, 255)",
"rgb(255, 0, 0)",
"rgb(0, 255, 0)",
"rgb(0, 0, 255)",
"rgb(255, 255, 0)",
"rgb(255, 0, 255)",
"rgb(0, 255, 255)",
"rgb(128, 0, 0)",
"rgb(0, 128, 0)",
"rgb(128, 128, 0)",
"rgb(128, 0, 128)",
"rgb(0, 128, 128)",
"rgb(255, 128, 0)",
"rgb(0, 255, 128)",
"rgb(128, 0, 255)",
"rgb(255, 0, 128)",
"rgb(128, 255, 0)",
"rgb(255, 128, 128)",
"rgb(128, 128, 255)"
]

let index_color_used = 0

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
        activeObject.set({fill:  color_list[index_color_used], stroke: stroke_list[index_color_used], lockMovementX: true, lockMovementY: true})
        canvas.renderAll()
      }
    }
    const handleRightClick = () => {
      const activeObject = canvas.getActiveObject()
      if (activeObject && activeObject.selectable) {
        if (activeObject.fill === color_list[index_color_used]) {
          activeObject.set({fill:  'rgb(0, 0, 0, 0)', stroke: 'rgb(0, 0, 0, 0)',lockMovementX: true, lockMovementY: true, borderColor: "rgba(0, 0, 0, 0)"})
        }
        else (activeObject.set({fill:  color_list[index_color_used], stroke: stroke_list[index_color_used],lockMovementX: true, lockMovementY: true}))
        canvas.renderAll()
      }
    }
    const handleMouseDown = (options: fabric.IEvent) => {
      // Check if it's a left-click (0) or right-click (2) event
      const mouseEvent = options.e as MouseEvent;
      const activeObject = canvas.getActiveObject()

      if (mouseEvent.button === 0) {
        if (activeObject && activeObject.selectable) {
          clearSelectionChange()
          handleLeftClick()
        }
      }
      else if (mouseEvent.button === 2) {
        handleRightClick()
      }
    }

     const handleSelection = (options: fabric.IEvent) => {
      const selectedObjects = canvas.getActiveObjects();
      if (selectedObjects.length > 0) {
        const mouseEvent = options.e as MouseEvent;
        if (mouseEvent.button === 0){
        clearSelectionChange()}
        selectedObjects.forEach(function (arrayItem) {
          if (arrayItem.selectable) {
            arrayItem.set({ fill: color_list[index_color_used], stroke: stroke_list[index_color_used]});
          }
        })
      }
      canvas.setActiveObject(selectedObjects[0])
      canvas.renderAll()
    }

      const clearSelectionChange = () => {
            const selectedObjects = canvas.getObjects();
            let LastColorExists = false;
            if (selectedObjects.length > 0) {
              selectedObjects.forEach(function (arrayItem) {
                if (arrayItem.selectable && arrayItem.fill === color_list[index_color_used]) {
                  LastColorExists = true
                }
              })
              if (LastColorExists){
                index_color_used += 1
              }
            }
          }

       document.onkeydown = function(e) {
        if (e.key === 'Backspace') {
          const selectedObjects = canvas.getObjects();
          if (selectedObjects.length > 0 && index_color_used > -1) {
            selectedObjects.forEach(function (arrayItem) {
              if ((arrayItem.selectable) && (arrayItem.fill === color_list[index_color_used])) {
                arrayItem.set({ fill: 'rgb(0, 0, 0, 0)', stroke: 'rgb(0,0,0,0)',lockMovementX: true, lockMovementY: true, borderColor: "rgba(0, 0, 0, 0)"});
              }
            })
            index_color_used = index_color_used - 1
            if (index_color_used == -1){
              index_color_used=0
            }
          }
          canvas.renderAll();
        }
    }

    canvas.on({'mouse:down': handleMouseDown, 'selection:created': handleSelection})
    return () => {
      canvas.off({'mouse:down': handleMouseDown, 'selection:created': handleSelection})
    }
  }
}

export default TransformTool




