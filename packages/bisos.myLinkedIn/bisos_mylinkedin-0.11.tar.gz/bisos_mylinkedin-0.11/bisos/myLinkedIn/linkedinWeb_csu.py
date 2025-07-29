# -*- coding: utf-8 -*-

""" #+begin_org
* ~[Summary]~ :: A =CS-Unit= as equivalent of facter in py and remotely with rpyc.
#+end_org """

####+BEGIN: b:py3:cs:file/dblockControls :classification "cs-u"
""" #+begin_org
* [[elisp:(org-cycle)][| /Control Parameters Of This File/ |]] :: dblk ctrls classifications=cs-u
#+BEGIN_SRC emacs-lisp
(setq-local b:dblockControls t) ; (setq-local b:dblockControls nil)
(put 'b:dblockControls 'py3:cs:Classification "cs-u") ; one of cs-mu, cs-u, cs-lib, bpf-lib, pyLibPure
#+END_SRC
#+RESULTS:
: cs-u
#+end_org """
####+END:

####+BEGIN: b:prog:file/proclamations :outLevel 1
""" #+begin_org
* *[[elisp:(org-cycle)][| Proclamations |]]* :: Libre-Halaal Software --- Part Of BISOS ---  Poly-COMEEGA Format.
** This is Libre-Halaal Software. © Neda Communications, Inc. Subject to AGPL.
** It is part of BISOS (ByStar Internet Services OS)
** Best read and edited  with Blee in Poly-COMEEGA (Polymode Colaborative Org-Mode Enhance Emacs Generalized Authorship)
#+end_org """
####+END:

####+BEGIN: b:prog:file/particulars :authors ("./inserts/authors-mb.org")
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars |]]* :: Authors, version
** This File: /bisos/git/bxRepos/bisos-pip/myLinkedIn/py3/bisos/myLinkedIn/linkedinWeb_csu.py
** File True Name: /bisos/git/auth/bxRepos/bisos-pip/myLinkedIn/py3/bisos/myLinkedIn/linkedinWeb_csu.py
** Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
#+end_org """
####+END:

####+BEGIN: b:py3:file/particulars-csInfo :status "inUse"
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars-csInfo |]]*
#+end_org """
import typing
csInfo: typing.Dict[str, typing.Any] = { 'moduleName': ['linkedinWeb_csu'], }
csInfo['version'] = '202505100515'
csInfo['status']  = 'inUse'
csInfo['panel'] = 'linkedinWeb_csu-Panel.org'
csInfo['groupingType'] = 'IcmGroupingType-pkged'
csInfo['cmndParts'] = 'IcmCmndParts[common] IcmCmndParts[param]'
####+END:

""" #+begin_org
* [[elisp:(org-cycle)][| ~Description~ |]] :: [[file:/bisos/git/auth/bxRepos/blee-binders/bisos-core/COMEEGA/_nodeBase_/fullUsagePanel-en.org][BISOS COMEEGA Panel]]
This a =Cs-Unit= for running the equivalent of facter in py and remotely with rpyc.
With BISOS, it is used in CMDB remotely.

** Relevant Panels:
** Status: In use with BISOS
** /[[elisp:(org-cycle)][| Planned Improvements |]]/ :
*** TODO complete fileName in particulars.
#+end_org """

####+BEGIN: b:prog:file/orgTopControls :outLevel 1
""" #+begin_org
* [[elisp:(org-cycle)][| Controls |]] :: [[elisp:(delete-other-windows)][(1)]] | [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[file:Panel.org][Panel]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]]

#+end_org """
####+END:

####+BEGIN: b:py3:file/workbench :outLevel 1
""" #+begin_org
* [[elisp:(org-cycle)][| Workbench |]] :: [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pyclbr %s" (bx:buf-fname))))][pyclbr]] || [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pydoc ./%s" (bx:buf-fname))))][pydoc]] || [[elisp:(python-check (format "/bisos/pipx/bin/pyflakes %s" (bx:buf-fname)))][pyflakes]] | [[elisp:(python-check (format "/bisos/pipx/bin/pychecker %s" (bx:buf-fname))))][pychecker (executes)]] | [[elisp:(python-check (format "/bisos/pipx/bin/pycodestyle %s" (bx:buf-fname))))][pycodestyle]] | [[elisp:(python-check (format "/bisos/pipx/bin/flake8 %s" (bx:buf-fname))))][flake8]] | [[elisp:(python-check (format "/bisos/pipx/bin/pylint %s" (bx:buf-fname))))][pylint]]  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: b:py3:cs:orgItem/basic :type "=PyImports= "  :title "*Py Library IMPORTS*" :comment "-- Framework and External Packages Imports"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  =PyImports=  [[elisp:(outline-show-subtree+toggle)][||]] *Py Library IMPORTS* -- Framework and External Packages Imports  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

# import os
import collections
# import invoke

####+BEGIN: b:py3:cs:framework/imports :basedOn "classification"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CsFrmWrk   [[elisp:(outline-show-subtree+toggle)][||]] *Imports* =Based on Classification=cs-u=
#+end_org """
from bisos import b
from bisos.b import cs
from bisos.b import b_io
from bisos.common import csParam

import collections
####+END:

# from bisos.facter import facter
# from bisos.banna import bannaPortNu

import pathlib
import re
import logging

import vobject
import random
import time

# from telemetry import Telemetry

from bisos.myLinkedIn import linkedinUtils
# from bisos.myLinkedIn import connections
from bisos.myLinkedIn import invitations
# from bisos.myLinkedIn import messages


# from bisos.myLinkedIn import messages_822

from bisos.myLinkedIn import linkedinWebInfo

logger = logging.getLogger(__name__)

####+BEGIN: b:py3:cs:orgItem/basic :type "=Executes=  "  :title "CSU-Lib Executions" :comment "-- cs.invOutcomeReportControl"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  =Executes=   [[elisp:(outline-show-subtree+toggle)][||]] CSU-Lib Executions -- cs.invOutcomeReportControl  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

cs.invOutcomeReportControl(cmnd=True, ro=True)

####+BEGIN: b:py3:cs:orgItem/section :title "Common Parameters Specification" :comment "based on cs.param.CmndParamDict -- As expected from CSU-s"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *Common Parameters Specification* based on cs.param.CmndParamDict -- As expected from CSU-s  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

def linkedinId_canonical(input: str,) -> str:
    return input


####+BEGIN: b:py3:cs:func/typing :funcName "commonParamsSpecify" :comment "~CSU Specification~" :funcType "ParSpc" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-ParSpc [[elisp:(outline-show-subtree+toggle)][||]] /commonParamsSpecify/  ~CSU Specification~  [[elisp:(org-cycle)][| ]]
#+end_org """
def commonParamsSpecify(
####+END:
        csParams: cs.param.CmndParamDict,
) -> None:
    csParams.parDictAdd(
        parName='account',
        parDescription="Account to be used for logging in.",
        parDataType=None,
        parDefault=None,
        parChoices=[],
        argparseShortOpt=None,
        argparseLongOpt='--account',
    )
    csParams.parDictAdd(
        parName='password',
        parDescription="Password to be used for logging in.",
        parDataType=None,
        parDefault=None,
        parChoices=[],
        argparseShortOpt=None,
        argparseLongOpt='--password',
    )
    csParams.parDictAdd(
        parName='browser',
        parDescription="Browser to be used.",
        parDataType=None,
        parDefault=None,
        parChoices=[],
        argparseShortOpt=None,
        argparseLongOpt='--browser',
    )
    csParams.parDictAdd(
        parName='browserProfilePath',
        parDescription="Profile name within Chrome.",
        parDataType=None,
        parDefault="~/.config/google-chrome/Default",
        parChoices=[],
        argparseShortOpt=None,
        argparseLongOpt='--browserProfilePath',
    )
    csParams.parDictAdd(
        parName='minInterval',
        parDescription="Minimum Interval in Seconds.",
        parDataType=None,
        parDefault=15,
        parChoices=[],
        argparseShortOpt=None,
        argparseLongOpt='--minInterval',
    )
    csParams.parDictAdd(
        parName='maxInterval',
        parDescription="Maximum Interval in Seconds.",
        parDataType=None,
        parDefault=35,
        parChoices=[],
        argparseShortOpt=None,
        argparseLongOpt='--maxInterval',
    )


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "Direct Command Services" :anchor ""  :extraInfo "Examples and CSs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _Direct Command Services_: |]]  Examples and CSs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "examples_csu" :comment "" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<examples_csu>>  =verify= ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class examples_csu(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, None).isProblematic():
            return failed(cmndOutcome)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Basic example command.
        #+end_org """)

        od = collections.OrderedDict
        cmnd = cs.examples.cmndEnter
        # literal = cs.examples.execInsert

        credsPars = od([('account', "someUser"), ('password', "somePasswd")])

        oneLinkedinUrl = '''https://www.linkedin.com/in/azad-sokhangoo-71b023365'''
        oneLinkedinId =  linkedinUtils.LinkedinId.fromUrl(oneLinkedinUrl)
        oneVCardsDir="~/bpos/usageEnvs/selected/myLinkedIn/selected/VCards"

        cs.examples.menuChapter('=LinkedIn Web Info=')

        cs.examples.menuSection('/ContactInfo From Url --- Exit All Chrome Windows/')

        cmnd('contactInfo', pars=credsPars,  args=oneLinkedinUrl)

        cmnd('contactInfoToVCard',
             pars=od([('vcardsDir', oneVCardsDir),]),
             args=oneLinkedinId)

        cmnd('contactInfoToVCard',
             pars=od([('vcardsDir', oneVCardsDir), ('account', "someUser"), ('password', "somePasswd")]),
             wrapper=f"ls -1 {oneVCardsDir} | egrep '.vcf$' | head -2 | sed 's/\.[^.]*$//' | ",
            )


        return(cmndOutcome)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "contactInfo" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "account password browser minInterval maxInterval" :argsMin 0 :argsMax 9999 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<contactInfo>>  =verify= parsOpt=account password browser minInterval maxInterval argsMax=9999 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class contactInfo(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ 'account', 'password', 'browser', 'minInterval', 'maxInterval', ]
    cmndArgsLen = {'Min': 0, 'Max': 9999,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             account: typing.Optional[str]=None,  # Cs Optional Param
             password: typing.Optional[str]=None,  # Cs Optional Param
             browser: typing.Optional[str]=None,  # Cs Optional Param
             minInterval: typing.Optional[str]=None,  # Cs Optional Param
             maxInterval: typing.Optional[str]=None,  # Cs Optional Param
             argsList: typing.Optional[list[str]]=None,  # CsArgs
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {'account': account, 'password': password, 'browser': browser, 'minInterval': minInterval, 'maxInterval': maxInterval, }
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
        account = csParam.mappedValue('account', account)
        password = csParam.mappedValue('password', password)
        browser = csParam.mappedValue('browser', browser)
        minInterval = csParam.mappedValue('minInterval', minInterval)
        maxInterval = csParam.mappedValue('maxInterval', maxInterval)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Returns runFacterAndGetJsonOutputBytes.
        #+end_org """)

        cmndArgs = self.cmndArgsGet("0&9999", cmndArgsSpecDict, argsList)

        def processArgsAndStdin(cmndArgs, process):
            for each in cmndArgs:
                process(each)
            stdinArgs = b_io.stdin.readAsList()
            for each in stdinArgs:
                process(each)

        # logging.basicConfig(level=logging.INFO)

        augmentor = linkedinWebInfo.LinkedInRemoteAugmentor(
            chrome_user_data_dir=pathlib.Path("~/.config/google-chrome").expanduser(),
            chrome_profile="Default"
        )

        augmentor.start_driver(account, password)

        def process(each):
            info = augmentor.fetch_contact_info(each)
            print(info)

        processArgsAndStdin(cmndArgs, process)

        augmentor.stop_driver()

        return cmndOutcome.set(opResults="DONE",)



####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&9999",
            argName="cmndArgs",
            argDefault=None,
            argChoices=[],
            argDescription="Path to the LinkedIn Basic_LinkedInDataExport_DATE.zip file."
        )

        return cmndArgsSpecDict


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "contactInfoToVCard" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "myLinkedInBase vcardsDir account password browser minInterval maxInterval" :argsMin 0 :argsMax 9999 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<contactInfoToVCard>>  =verify= parsOpt=myLinkedInBase vcardsDir account password browser minInterval maxInterval argsMax=9999 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class contactInfoToVCard(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ 'myLinkedInBase', 'vcardsDir', 'account', 'password', 'browser', 'minInterval', 'maxInterval', ]
    cmndArgsLen = {'Min': 0, 'Max': 9999,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             myLinkedInBase: typing.Optional[str]=None,  # Cs Optional Param
             vcardsDir: typing.Optional[str]=None,  # Cs Optional Param
             account: typing.Optional[str]=None,  # Cs Optional Param
             password: typing.Optional[str]=None,  # Cs Optional Param
             browser: typing.Optional[str]=None,  # Cs Optional Param
             minInterval: typing.Optional[str]=None,  # Cs Optional Param
             maxInterval: typing.Optional[str]=None,  # Cs Optional Param
             argsList: typing.Optional[list[str]]=None,  # CsArgs
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {'myLinkedInBase': myLinkedInBase, 'vcardsDir': vcardsDir, 'account': account, 'password': password, 'browser': browser, 'minInterval': minInterval, 'maxInterval': maxInterval, }
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
        myLinkedInBase = csParam.mappedValue('myLinkedInBase', myLinkedInBase)
        vcardsDir = csParam.mappedValue('vcardsDir', vcardsDir)
        account = csParam.mappedValue('account', account)
        password = csParam.mappedValue('password', password)
        browser = csParam.mappedValue('browser', browser)
        minInterval = csParam.mappedValue('minInterval', minInterval)
        maxInterval = csParam.mappedValue('maxInterval', maxInterval)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Takes input from stdin or args, for each vcard updates email if needed.
        #+end_org """)

        cmndArgs = self.cmndArgsGet("0&9999", cmndArgsSpecDict, argsList)

        def processArgsAndStdin(cmndArgs, process):
            for each in cmndArgs:
                process(each)
            stdinArgs = b_io.stdin.readAsList()
            # if the list was sorted, we shuffle it
            random.shuffle(stdinArgs)
            for each in stdinArgs:
                process(each)

        # logging.basicConfig(level=logging.DEBUG)
        logging.basicConfig(level=logging.INFO)

        augmentor = linkedinWebInfo.LinkedInRemoteAugmentor(
            chrome_user_data_dir=pathlib.Path("~/.config/google-chrome").expanduser(),
            chrome_profile="Default"
        )

        augmentor.start_driver(account, password)

        def process(linkedinId):
            waitBeforeNext = augmentVcardFromLinkedin(augmentor, linkedinId, vcardsDir)
            if waitBeforeNext == False:
                return
            waitInterval = random.randint(minInterval, maxInterval)
            print(f"Waiting for waitInterval={waitInterval} Seconds")
            time.sleep(waitInterval)

        processArgsAndStdin(cmndArgs, process)

        augmentor.stop_driver()

        return cmndOutcome.set(opResults="DONE",)


####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()

        cmndArgsSpecDict.argsDictAdd(
            argPosition="0&9999",
            argName="cmndArgs",
            argDefault=None,
            argChoices=[],
            argDescription="Path to the LinkedIn Basic_LinkedInDataExport_DATE.zip file."
        )

        return cmndArgsSpecDict


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "Support Functions" :anchor ""  :extraInfo ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _Support Functions_: |]]    [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:func/typing :funcName "augmentVcardFromLinkedin" :funcType "extTyped" :deco "track"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /augmentVcardFromLinkedin/  deco=track  [[elisp:(org-cycle)][| ]]
#+end_org """
@cs.track(fnLoc=True, fnEntry=True, fnExit=True)
def augmentVcardFromLinkedin(
####+END:
        augmentor: linkedinWebInfo.LinkedInRemoteAugmentor,
        linkedinId: str,
        vcardsDir: pathlib.Path,
    ) -> bool:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ] Extracts contact info from LinkedIn and augments the corresponding vCard file.
The vCard file is assumed to be named <linkedinId>.vcf inside vcard_dir.
#+end_org """

    waitBeforeNext = True

    linkedinUrl = linkedinUtils.LinkedinId.toUrl(linkedinId)
    vcardsdDirPath = pathlib.Path(f"{vcardsDir}").expanduser().resolve()

    vcardPath = linkedinUtils.VCard.find_vcard(vcardsdDirPath, linkedinId)

    if vcardPath ==  None:
        print(f"Missing {linkedinId} VCard Skipped")
        waitBeforeNext = False
        return waitBeforeNext

    vcardStr  = vcardPath.read_text(encoding="utf-8").strip()
    vcard = vobject.readOne(vcardStr)

    field = "email"
    if hasattr(vcard, field):
        value = vcard.contents[field][0].value
        print(f"linkedinId={linkedinId} -- email = {value} -- Skipped")
        waitBeforeNext = False
        return waitBeforeNext

    logger.info(f"Augmenting vCard from LinkedIn URL: {linkedinUrl}")
    contact_info = augmentor.fetch_contact_info(linkedinUrl)

    linkedinUtils.VCard.augment_vcard_with_contact_info(vcardPath, contact_info)
    waitBeforeNext = True
    return waitBeforeNext

####+BEGIN: b:py3:cs:framework/endOfFile :basedOn "classification"
""" #+begin_org
* [[elisp:(org-cycle)][| *End-Of-Editable-Text* |]] :: emacs and org variables and control parameters
#+end_org """

#+STARTUP: showall

### local variables:
### no-byte-compile: t
### end:
####+END:
