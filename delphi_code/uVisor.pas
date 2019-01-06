unit uVisor;

interface

uses
  System.SysUtils, System.Types, System.UITypes, System.Classes, System.Variants,
  FMX.Types, FMX.Controls, FMX.Forms, FMX.Graphics, FMX.Dialogs, Web.HTTPApp,
  Web.HTTPProd, FMX.WebBrowser, FMX.Controls.Presentation, FMX.StdCtrls,System.Win.Registry,
  FMX.Edit;

type
  TForm1 = class(TForm)
    Panel1: TPanel;
    WebBrowser1: TWebBrowser;
    PageProducer1: TPageProducer;
    Timer1: TTimer;
    Button1: TButton;
    Label1: TLabel;
    Edit1: TEdit;
    procedure Timer1Timer(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure PageProducer1HTMLTag(Sender: TObject; Tag: TTag;
      const TagString: string; TagParams: TStrings; var ReplaceText: string);
    procedure Button1Click(Sender: TObject);
  private
    { Private declarations }
    procedure SetPermissions;
  public
    { Public declarations }
  end;

var
  Form1: TForm1;

implementation

{$R *.fmx}

procedure TForm1.Button1Click(Sender: TObject);
var
  html:TStringList;
begin
  html := TStringList.Create;

  html.Text := PageProducer1.Content;
  html.SaveToFile('C:/temp360/test.html');


   html.Free;
  Timer1.Enabled := True;
end;

procedure TForm1.FormShow(Sender: TObject);
begin
SetPermissions;
Label1.Text := ParamStr(1);
end;

procedure TForm1.PageProducer1HTMLTag(Sender: TObject; Tag: TTag;
  const TagString: string; TagParams: TStrings; var ReplaceText: string);
begin
if TagString = 'pano' then
    ReplaceText := '"' + Edit1.Text + Label1.Text + '"';
end;

procedure TForm1.SetPermissions;
const
  cHomePath = 'SOFTWARE';
  cFeatureBrowserEmulation =
    'Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BROWSER_EMULATION\';
  cIE11 = 11001;

var
  Reg: TRegIniFile;
  sKey: string;
begin

  sKey := ExtractFileName(ParamStr(0));
  Reg := TRegIniFile.Create(cHomePath);
  try
    if Reg.OpenKey(cFeatureBrowserEmulation, True) and
      not(TRegistry(Reg).KeyExists(sKey) and (TRegistry(Reg).ReadInteger(sKey)
      = cIE11)) then
      TRegistry(Reg).WriteInteger(sKey, cIE11);
  finally
    Reg.Free;
  end;

  end;

procedure TForm1.Timer1Timer(Sender: TObject);
begin
  Timer1.Enabled := False;
  WebBrowser1.URL := 'file://C:/temp360/test.html';
  WebBrowser1.Navigate;
end;


end.
