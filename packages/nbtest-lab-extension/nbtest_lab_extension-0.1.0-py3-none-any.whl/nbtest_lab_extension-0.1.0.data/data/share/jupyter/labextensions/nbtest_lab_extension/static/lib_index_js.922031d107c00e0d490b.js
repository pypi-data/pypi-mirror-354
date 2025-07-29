"use strict";
(self["webpackChunknbtest_lab_extension"] = self["webpackChunknbtest_lab_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_7__);








class ToggleSignal {
    constructor() {
        this._stateChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
    }
    get stateChanged() {
        return this._stateChanged;
    }
    emitState(value) {
        this._stateChanged.emit(value);
    }
}
const toggleSignal = new ToggleSignal();
let status = 0; // 🔹 Track status locally, starts at 0
const plugin = {
    id: 'nbtest_lab_extension',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__.IRenderMimeRegistry],
    activate: (app, palette, tracker, rendermime) => {
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
                const outputModel = new _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__.OutputAreaModel();
                const outputArea = new _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__.OutputArea({
                    model: outputModel,
                    rendermime: rendermime
                });
                // Python code to toggle environment variable
                const code = `
import os
os.environ["NBTEST_RUN_ASSERTS"] = "1" if os.environ.get("NBTEST_RUN_ASSERTS", "0") != "1" else "0"
        `;
                // Execute the code inside the kernel using OutputArea
                _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__.OutputArea.execute(code, outputArea, currentNotebook.sessionContext)
                    .then((msg) => {
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
            var _a;
            const getTestLogMap = async (notebookPath) => {
                const dir = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_7__.PathExt.dirname(notebookPath);
                const response = await fetch(`files/${dir}/test_log.csv`);
                if (!response.ok) {
                    return new Map();
                }
                const text = await response.text();
                const lines = text.trim().split('\n');
                const map = new Map();
                lines.slice(1).forEach(line => {
                    const [id, status] = line.split(',');
                    map.set(id.trim(), parseInt(status.trim(), 10));
                });
                return map;
            };
            const parseTestIds = (source, cellIndex) => {
                const lines = source.split('\n');
                const ids = [];
                lines.forEach((line, i) => {
                    const match = line.match(/nbtest\.assert_\w+.*?test_id\s*=\s*['"]?([\w\d_]+)['"]?/);
                    if (match) {
                        ids.push(match[1]);
                    }
                    else if (line.includes('nbtest.assert_')) {
                        ids.push(`${cellIndex}_${i}`);
                    }
                });
                return ids;
            };
            const displayTestResults = async () => {
                const notebookPath = panel.context.path;
                const testMap = await getTestLogMap(notebookPath);
                const notebook = panel.content;
                notebook.widgets.forEach((cell, index) => {
                    const model = cell.model;
                    if (!(model instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_6__.CodeCellModel)) {
                        return;
                    }
                    const source = model.sharedModel.getSource();
                    const testIds = parseTestIds(source, index);
                    let pass = 0, fail = 0, error = 0;
                    testIds.forEach(id => {
                        const result = testMap.get(id);
                        if (result === 1) {
                            pass++;
                        }
                        else if (result === 0) {
                            fail++;
                        }
                        else if (result === -1) {
                            error++;
                        }
                    });
                    const existing = cell.node.querySelector('.nbtest-result');
                    if (existing) {
                        existing.remove();
                    }
                    if (testIds.length > 0) {
                        const badge = document.createElement('div');
                        badge.className = 'nbtest-result';
                        badge.textContent = `✅ ${pass} | ❌ ${fail} | ⚠️ ${error}`;
                        badge.style.fontSize = '0.8em';
                        badge.style.margin = '4px 0 4px 4px';
                        badge.style.padding = '2px 8px';
                        badge.style.borderRadius = '4px';
                        badge.style.backgroundColor = 'rgba(101, 123, 131, 0.12)';
                        badge.style.color = '#586e75';
                        badge.style.display = 'inline-block';
                        cell.node.insertBefore(badge, cell.node.firstChild);
                    }
                });
            };
            // 🔹 Call test results display after highlighting
            displayTestResults();
            // 🔹 Optionally refresh on notebook execution or kernel idle
            panel.sessionContext.statusChanged.connect((_, kernelStatus) => {
                if (kernelStatus === 'idle') {
                    displayTestResults();
                }
            });
            console.log('Notebook opened: Adding Toggle Asserts button');
            if (Array.from(panel.toolbar.names()).includes('toggleAsserts')) {
                console.log('Button already exists');
                return;
            }
            // 🔹 Create status display widget
            const statusDisplay = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Widget();
            statusDisplay.node.textContent = 'NBTest status: OFF'; // Initial value
            statusDisplay.node.style.marginLeft = '8px'; // Add spacing
            const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
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
                    const source = model instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_6__.CodeCellModel ? model.sharedModel.getSource() : '';
                    const node = cell.node;
                    if (/nbtest\.assert_\w+/.test(source)) {
                        node.style.borderLeft = '4px solid #f39c12';
                        node.style.backgroundColor = 'rgba(181, 137, 0, 0.12)';
                    }
                    else {
                        node.style.borderLeft = '';
                        node.style.backgroundColor = '';
                    }
                });
            };
            // 🔹 Run once on notebook load
            highlightAssertCells();
            // 🔹 Re-check on cell add/remove
            (_a = panel.content.model) === null || _a === void 0 ? void 0 : _a.cells.changed.connect(() => {
                highlightAssertCells();
            });
            // 🔹 Also re-check on content edits
            panel.content.activeCellChanged.connect(() => {
                var _a;
                const activeModel = (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.model;
                if (activeModel instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_6__.CodeCellModel) {
                    activeModel.sharedModel.changed.connect(() => {
                        highlightAssertCells();
                    });
                }
            });
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.922031d107c00e0d490b.js.map