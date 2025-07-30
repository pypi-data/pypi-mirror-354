import { ReactWidget } from '@jupyterlab/apputils';
import { FileBrowserModel } from '@jupyterlab/filebrowser';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { TranslationBundle } from '@jupyterlab/translation';
import { CommandRegistry } from '@lumino/commands';
import { Message } from '@lumino/messaging';
import { Widget } from '@lumino/widgets';
import * as React from 'react';
import { GitPanel } from '../components/GitPanel';
import { GitExtension } from '../model';
import { gitWidgetStyle } from '../style/GitWidgetStyle';

/**
 * A class that exposes the git plugin Widget.
 */
export class GitWidget extends ReactWidget {
  constructor(
    model: GitExtension,
    settings: ISettingRegistry.ISettings,
    commands: CommandRegistry,
    fileBrowserModel: FileBrowserModel,
    trans: TranslationBundle,
    options?: Widget.IOptions
  ) {
    super();
    this.node.id = 'GitSession-root';
    this.addClass(gitWidgetStyle);

    this._trans = trans;
    this._commands = commands;
    this._fileBrowserModel = fileBrowserModel;
    this._model = model;
    this._settings = settings;

    // Add refresh standby condition if this widget is hidden
    model.refreshStandbyCondition = (): boolean =>
      !this._settings.composite['refreshIfHidden'] && this.isHidden;
  }

  /**
   * A message handler invoked on a `'before-show'` message.
   *
   * #### Notes
   * The default implementation of this handler is a no-op.
   */
  onBeforeShow(msg: Message): void {
    // Trigger refresh when the widget is displayed
    this._model.refresh().catch(error => {
      console.error('Fail to refresh model when displaying GitWidget.', error);
    });
    super.onBeforeShow(msg);
  }

  /**
   * Render the content of this widget using the virtual DOM.
   *
   * This method will be called anytime the widget needs to be rendered, which
   * includes layout triggered rendering.
   */
  render(): JSX.Element {
    return (
      <GitPanel
        commands={this._commands}
        filebrowser={this._fileBrowserModel}
        model={this._model}
        settings={this._settings}
        trans={this._trans}
      />
    );
  }

  private _commands: CommandRegistry;
  private _fileBrowserModel: FileBrowserModel;
  private _model: GitExtension;
  private _settings: ISettingRegistry.ISettings;
  private _trans: TranslationBundle;
}
