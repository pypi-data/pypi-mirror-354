import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  LabShell,
} from "@jupyterlab/application";
// import IRenderMimeRegistry from "@jupyterlab/rendermime";
import { INotebookTracker, NotebookPanel } from "@jupyterlab/notebook";
import $ from "jquery";
import { CodeCellModel, MarkdownCell } from "@jupyterlab/cells";
import { IDocumentManager } from "@jupyterlab/docmanager";

// EXAMPLE TEST LINK
// Note the lock and qualtrics params
// http://localhost:8888/lab/tree/E1/we-co-na.ipynb?reset&lock=1&qualtrics=1


//TODO notes
//- propose ripping out anything stateful. Pass all that in via query params
//- 

const viewWeTitle = "Click here to see examples from your first notebook";
const urlParams = new URLSearchParams(window.location.search);
const user = getUrlUser();
const hubLink =
  urlParams.get("hub") +
  "/" +
  user +
  "/" +
  urlParams.get("index") +
  "/" +
  urlParams.get("condition");
const qualtricsParam = urlParams.get("qualtrics")
const reloadBlockParam = urlParams.get("rb");

let isInternalLinkGenerated = false;

// Hide UI elements to effect lockdown
function lockdown(this: LabShell) {

  if (reloadBlockParam === "1") {
    let main = document.getElementById("main");
    if (main) main.style.display = "none"
    window.alert("You cannot reload this tab.\n\nPlease return to the experiment tab to continue.\n\nYou may close this tab now.");
  }

  //try to collapse left navbar again. It seems sometimes a delayed workspace load will pop it out agains
  this.collapseLeft();

  let top_panel = document.getElementById("jp-top-panel");
  if (top_panel) top_panel.style.display = "none";

  let left_stack = document.getElementById("jp-left-stack");
  if (left_stack) left_stack.style.display = "none";

  let statusbar = document.getElementById("jp-main-statusbar");
  if (statusbar) statusbar.style.display = "none";

  let main_panel = document.getElementById("jp-main-content-panel");
  if (main_panel) {
    if (main_panel.children.length > 0) {
      let first_child = main_panel.children[0];
      (first_child as HTMLElement).style.display = "none";
    }
  }
}

function getUrlUser() {
  let pathArray = window.location.pathname.split("/");
  let userPathIndex = 0;
  pathArray.forEach((path, index) => {
    if (path === "user") {
      userPathIndex = index + 1;
    }
  });
  return pathArray[userPathIndex];
}

/**
 *
 * @param notebook
 * Remove external link from worked example since it's
 * only available for reference
 */
const clearExternalLink = (notebook: NotebookPanel) => {
  const notebookModel = notebook.model;
  if (notebookModel) {
    const lastCell = notebookModel.cells.get(notebookModel.cells.length - 1);
    if (lastCell.id.includes("external")) {
      console.log("Clearing unused worked example external link.");
    }
  }
};

const generateLinks = (
  notebooks: INotebookTracker,
  docManager: IDocumentManager
) => {
  const notebook = notebooks.currentWidget;
  let title = "";
  if (notebook) title = notebook.title.label;

  let notebookModel = null;
  if (notebook) notebookModel = notebook.model;
  let link = "";
  let doesInternalLinkExist = false;

  if (notebookModel) {
    try {
      let first_cell = notebookModel.cells.get(0);
      let first_cell_json_source = first_cell.toJSON().source;//[0];
      doesInternalLinkExist = first_cell_json_source.includes(viewWeTitle);
    } catch (err) {
      console.log(err);
    }
  }

  if (
    title.includes("ps-near1") &&
    !doesInternalLinkExist &&
    !isInternalLinkGenerated
  ) {
    notebooks.forEach((notebook) => {
      if (notebook.title.label.includes("we-")) {
        clearExternalLink(notebook);
      }
    });
    if (title.includes("-gl")) {
      let bl_param = urlParams.get("bl");
      if (bl_param && Number.parseInt(bl_param) === 1) {
        link = `<span style="font-size:16pt;">[${viewWeTitle}](we-bl-gl.ipynb)</span>`;
      } else {
        link = `<span style="font-size:16pt;">[${viewWeTitle}](we-co-gl.ipynb)</span>`;
      }
    }
    if (title.includes("-na")) {
      let bl_param = urlParams.get("bl");
      if (bl_param && Number.parseInt(bl_param) === 1) {
        link = `<span style="font-size:16pt;">[${viewWeTitle}](we-bl-na.ipynb)</span>`;
      } else {
        link = `<span style="font-size:16pt;">[${viewWeTitle}](we-co-na.ipynb)</span>`;
      }
    }
    // For PS1, adds link to WE at top
    if (notebook) {
      notebook.context.model.sharedModel.insertCell(0, {
        cell_type: "markdown",
        source: [link],
        metadata: {
          deletable: false,
          editable: false,
        },
        id: "internal-we",
      });
    }
  }

  if (!$("#external-link").length) {
    const $link = $("<a>", {
      id: "external-link",
      css: {
        color: "#64b5f6",
        fontSize: "16pt",
      },
    });
    $link.text(
      "Click here after you've finished to move to the next assignment"
    );
    $link.on("click", function () {
      // do save: if page navigation occurs in an unsaved state, "unsaved changes" popup will appear
      let savePromises: Promise<void>[] = [];
      notebooks.forEach((notebook) => {
        let context = docManager.contextForWidget(notebook);
        if (context) {
          let savePromise = context.save();
          savePromises.push(savePromise);
        }
      });
      //wait for all save promises
      //qualtrics integration: do not return to hub
      if (qualtricsParam === "1") {
        Promise.all(savePromises).then(() => {
          //hide the interface
          //$(".jp-LabShell").hide(); //hidden = true; /
          let main = document.getElementById("main")
          if (main) main.style.display = "none"

          //muck with the history/query params to prevent unhiding via reload
          urlParams.set("rb", "1");
          var newRelativePathQuery = window.location.pathname + '?' + urlParams.toString();
          history.replaceState(null, '', newRelativePathQuery);

          //reveal instructions in popup since we have no HTML canvas to display on now
          //Playing around with the idea of keywords; would be easy to cut out
          let keywords = ["rain", "insure", "silk", "contest", "polish"];
          let keyword = "";
          if (title.includes("we-")) { keyword = keywords[0]; }
          else if (title.includes("ps-near1")) { keyword = keywords[1]; }
          else if (title.includes("ps-near2")) { keyword = keywords[2]; }
          else if (title.includes("ps-far-")) { keyword = keywords[3]; }
          else if (title.includes("ps-farplus")) { keyword = keywords[4]; }
          window.alert("The keyword is:\n\n" + keyword + "\n\nPlease enter the keyword in the experiment tab to continue.\n\nClose this window *after* you enter the keyword in the experiment tab.");
          //no keyword version: window.alert("Please return to the experiment tab to continue.\n\nYou may close this tab now.");
        });
      } else {
        //Wes original functionality
        Promise.all(savePromises).then(() => window.location.replace(hubLink));
      }
    });
    // JLab 1.2.x attachement point; requires scroll into view in Jlab 4.x
    // const $notebook = $(".jp-NotebookPanel-notebook");
    const $notebook = $(".jp-WindowedPanel-outer");
    $notebook.append($link);
  }
};

// };
/**
 * Initialization data for the experimental-control extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'datawhys_experimental_control:plugin',
  description: 'A JupyterLab extension that locks down the user interface and provides additional controls for running experiments using the JupyterLab platform. It is not configurable but may serve as an example for other projects.',
  autoStart: true,
  requires: [INotebookTracker, IDocumentManager],
  activate: (
    app: JupyterFrontEnd,
    notebooks: INotebookTracker,
    docManager: IDocumentManager
  ) => {
    const urlParams = new URLSearchParams(window.location.search);
    const lockParam = urlParams.get("lock");
    const agentImageParam = urlParams.get("personalagent");

    if (lockParam === "1") {
      console.log("JupyterLab extension datawhys_experimental_control is activated!");

      // Generate notebook links - very specific to DataWhys E1 experiment!
      notebooks.currentChanged.connect(() => {
        let widget = notebooks.currentWidget;
        if (widget) widget.context.ready.then(() => {
          generateLinks(notebooks, docManager);
        });
      });

      // Remove 'x' icon from tab and Launcher tab here since we need app context
      app.restored.then(() => {
        //collapse the file explorer and anything else on the left navbar
        (app.shell as LabShell).collapseLeft();

        //Wes: why set a timer here; why not wait for currentChanged as below?
        setInterval(function () {
          //prevent adding new notebooks
          $(".lm-TabBar-addButton").hide();
          // $(".p-TabBar-tabCloseIcon").hide();
          $(".lm-TabBar-tabCloseIcon").hide();
          let workedExampleEligible = true;
          // $(".p-TabBar-tab").each(function (idx) {
          $(".lm-TabBar-tab").each(function (idx) {
            let $currentTabParent = $(this);
            let $currentTab = $currentTabParent[0];
            let $innerText = $currentTab.innerText;
            if ($innerText.includes("near2") || $innerText.includes("far")) {
              workedExampleEligible = false;
            }
          });

          // $(".p-TabBar-tab").each(function (idx) {
          $(".lm-TabBar-tab").each(function (idx) {
            let $currentTabParent = $(this);
            let $currentTab = $currentTabParent[0];
            let $innerText = $currentTab.innerText;
            if (
              !($innerText.includes("we-") || $innerText.includes("near1")) ||
              !workedExampleEligible
            ) {
              $currentTabParent.hide();
            }
          });

          //Oct 2023: auto render any markdown cells
          // The following builtin method unfortunately steals focus
          // NotebookActions.renderAllMarkdown(notebooks.currentWidget.content)
          let widget = notebooks.currentWidget;
          if (widget) widget.content.widgets.forEach((child, index) => {
            if (child.model.type === 'markdown') {
              (child as MarkdownCell).rendered = true;
              child.inputHidden = false;
              // Signal does not appear needed; the comment below is for reference
              // executed.emit({ notebook, cell, success: true });
            }
          });

          //Jan 2022: force every cell of WE and PS1 be attempted in order to allow moving off the notebook
          //NOTE: previous version checked that all code cells were attempted, which was flexible but has the 
          //edge case of them creating a dummy code cell that logically does not need to be filled for completeness
          if (workedExampleEligible) {
            //hide the exit link by default for WE and PS1
            $("#external-link").hide();

            // Count code cells attempted (non-blank) in the active notebook
            let codeCellAttemptedCount = 0;

            let model = notebooks?.currentWidget?.model;
            if (model) {
              for (let j = 0; j < model.cells.length; j++) {
                // Count a non-blank code cell
                let result = model.cells.get(j);
                if (result.type === 'code' && result.sharedModel.source !== "") {
                  //Oct 2023: check if cell has been executed in addition to being nonempty
                  let codeCell = result as CodeCellModel;
                  if (codeCell.executionCount && codeCell.executionCount > 0) {
                    codeCellAttemptedCount++;
                  }

                }
              }
            }

            // For checking our count, we need to be specific about what notebook we're looking at because they have different #s of code cells
            let allCodeCellsAttempted = false;
            let widget = notebooks.currentWidget;
            if (widget && widget.title.label.includes("we-") && codeCellAttemptedCount >= 9) { //Was 10 before dataframe display removed 11/22
              allCodeCellsAttempted = true;
            } else if (widget && widget.title.label.includes("near1") && codeCellAttemptedCount >= 5) {
              allCodeCellsAttempted = true;
            }


            if (allCodeCellsAttempted) {
              $("#external-link").show();
            }
          // WE and PS1 are worked example eligible; if we are on a non-eligible notebook, show link
          } else {
            $("#external-link").show();
          }
          // 6/6/2025, Farshid thesis experiment
          // He was using getElementById in the metadata extension to swap out images dynamically.
          // It looks like the React backing of JLab 4 is affecting the lifecycle of the DOM such that
          // images lower in the page return null with getElementById even after their onload events have fired
          // It seems the best way to get the old behavior is to use id tags, e.g. agent-img-x, check these continuously,
          // and set the src appropriately if it is not correct
          // if agent image param is set
          if (agentImageParam != null) {
            // iterate over 5 images
            for (let i = 1; i <= 5; i++) {
              let element = document.getElementById(`agent-img-${i}`);
              // if one exists
              if (element) {
                let agent_image = element as HTMLImageElement;
                // change its src
                if (agent_image.src == "") {
                  agent_image.src = 'https://ffarzan.com/wp-content/uploads/2025/03/jup-' + agentImageParam + `-${i}.jpg`;
                }
              }
            }
          }
        }, 1000);
      });

      notebooks.currentChanged.connect(lockdown, app.shell);
    }
  },
};

export default extension;