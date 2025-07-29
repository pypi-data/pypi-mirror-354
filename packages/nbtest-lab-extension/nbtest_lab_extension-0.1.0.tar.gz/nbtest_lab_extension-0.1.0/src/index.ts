import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICommandPalette, ToolbarButton } from '@jupyterlab/apputils';
import { INotebookTracker } from '@jupyterlab/notebook';
import { KernelMessage } from '@jupyterlab/services';
import { OutputArea, OutputAreaModel } from '@jupyterlab/outputarea';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { Signal } from '@lumino/signaling';
import { Widget } from '@lumino/widgets';
import { CodeCellModel } from '@jupyterlab/cells';

class ToggleSignal {
  private _stateChanged = new Signal<this, string>(this);

  get stateChanged() {
    return this._stateChanged;
  }

  emitState(value: string) {
    this._stateChanged.emit(value);
  }
}

const toggleSignal = new ToggleSignal();
let status = 0; // 🔹 Track status locally, starts at 0

const plugin: JupyterFrontEndPlugin<void> = {
  id: 'nbtest_lab_extension',
  autoStart: true,
  requires: [ICommandPalette, INotebookTracker, IRenderMimeRegistry],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    tracker: INotebookTracker,
    rendermime: IRenderMimeRegistry
  ) => {
    const { commands } = app;
    const command = 'nbtest:toggle-asserts';

    commands.addCommand(command, {
      label: 'Toggle NBTEST_RUN_ASSERTS',
      execute: async () => {
        const currentNotebook = tracker.currentWidget;
        if (!currentNotebook) {
          console.error('No active notebook.');
          return;
        }

        const session = currentNotebook.sessionContext.session;
        if (!session || !session.kernel) {
          console.error('No active kernel.');
          return;
        }

        // Initialize OutputArea to display execution results
        const outputModel = new OutputAreaModel();
        const outputArea = new OutputArea({
          model: outputModel,
          rendermime: rendermime
        });

        // Python code to toggle environment variable
        const code = `
import os
os.environ["NBTEST_RUN_ASSERTS"] = "1" if os.environ.get("NBTEST_RUN_ASSERTS", "0") != "1" else "0"
        `;

        // Execute the code inside the kernel using OutputArea
        OutputArea.execute(code, outputArea, currentNotebook.sessionContext)
          .then((msg: KernelMessage.IExecuteReplyMsg | undefined) => {
            console.log('Execution complete:', msg);
          })
          .catch(reason => console.error('Execution error:', reason));

        // 🔹 Toggle status variable locally
        status = status === 0 ? 1 : 0;
        const newStatus = status === 1 ? 'ON' : 'OFF';

        // 🔹 Emit updated status
        toggleSignal.emitState(newStatus);
      }
    });

    palette.addItem({ command, category: 'NBTest' });

    tracker.widgetAdded.connect((sender, panel) => {
      console.log('Notebook opened: Adding Toggle Asserts button');

      if (Array.from(panel.toolbar.names()).includes('toggleAsserts')) {
        console.log('Button already exists');
        return;
      }

      // 🔹 Create status display widget
      const statusDisplay = new Widget();
      statusDisplay.node.textContent = 'NBTest status: OFF'; // Initial value
      statusDisplay.node.style.marginLeft = '8px'; // Add spacing

      const button = new ToolbarButton({
        label: 'Toggle Asserts',
        tooltip: 'Toggle NBTEST_RUN_ASSERTS',
        onClick: async () => {
          console.log('Button clicked - toggling variable...');
          await commands.execute(command);
          await new Promise(resolve => setTimeout(resolve, 500));
        }
      });

      panel.toolbar.addItem('toggleAsserts', button);
      panel.toolbar.addItem('assertsStatus', statusDisplay); // 🔹 Add text display next to button

      // 🔹 Subscribe to signal and update the status display
      toggleSignal.stateChanged.connect((_, state) => {
        statusDisplay.node.textContent = `NBTest status: ${state}`;
      });

      // 🔹 Detect kernel restarts and reset NBTest status
      panel.sessionContext.statusChanged.connect((_, statusChanged) => {
        if (['starting', 'restarting'].includes(statusChanged)) {
          status = 0;
          toggleSignal.emitState('OFF');
        }
      });

      const highlightAssertCells = () => {
        const notebook = panel.content;
        notebook.widgets.forEach(cell => {
          const model = cell.model;
          const source =
            model instanceof CodeCellModel ? model.sharedModel.getSource() : '';
          const node = cell.node;

          if (/nbtest\.assert_\w+/.test(source)) {
            node.style.borderLeft = '4px solid #f39c12';
            node.style.backgroundColor = 'rgba(181, 137, 0, 0.12)';
          } else {
            node.style.borderLeft = '';
            node.style.backgroundColor = '';
          }
        });
      };

      // 🔹 Run once on notebook load
      highlightAssertCells();

      // 🔹 Re-check on cell add/remove
      panel.content.model?.cells.changed.connect(() => {
        highlightAssertCells();
      });

      // 🔹 Also re-check on content edits
      panel.content.activeCellChanged.connect(() => {
        const activeModel = panel.content.activeCell?.model;
        if (activeModel instanceof CodeCellModel) {
          activeModel.sharedModel.changed.connect(() => {
            highlightAssertCells();
          });
        }
      });
    });
  }
};

export default plugin;
