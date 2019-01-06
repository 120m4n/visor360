program Visor360;

uses
  System.StartUpCopy,
  FMX.Forms,
  uVisor in 'uVisor.pas' {Form1};

{$R *.res}

begin
  Application.Initialize;
  Application.CreateForm(TForm1, Form1);
  Application.Run;
end.
